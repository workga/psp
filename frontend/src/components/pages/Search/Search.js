import React, { useState, useEffect, useContext } from 'react';
import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import './Search.css';
import { ProductModal, CreateProductModal } from "./ProductModal.js"
import { AuthModal, AuthButton } from "./../../common/Auth.js"
import { AuthContext } from "./../../../context/AuthProvider.js"

export function Search() {
	const { auth, setAuth } = useContext(AuthContext);

  const [brands, setBrands] = useState([]);
  const [models, setModels] = useState([]);
  const [gens, setGens] = useState([]);
  const [categories, setCategories] = useState([])
  const [types, setTypes] = useState([])

  const [selectedBrandId, setSelectedBrandId] = useState('');
  const [selectedModelId, setSelectedModelId] = useState('');
  const [selectedGenId, setSelectedGenId] = useState('');
	const [selectedCategoryId, setSelectedCategoryId] = useState('');
	const [selectedTypeId, setSelectedTypeId] = useState('');

  const [brandSearch, setBrandSearch] = useState('');
  const [modelSearch, setModelSearch] = useState('');
  const [genSearch, setGenSearch] = useState('');
	const [categorySearch, setCategorySearch] = useState('');
	const [typeSearch, setTypeSearch] = useState('');


  const [searchResults, setSearchResults] = useState([]);

  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productModalActive, setProductModalActive] = useState(false);
  const [authModalActive, setAuthModalActive] = useState(false);
  const [createProductModalActive, setCreateProductModalActive] = useState(false);

  useEffect(() => {
    async function fetchBrands() {
      try {
        const response = await axios.get('/api/cars/brands', {
          params: { search: brandSearch, sort_by: 'score' }
        });
        setBrands(response.data);
      } catch (error) {
        console.error('Error fetching car brands:', error);
      }
    }

    fetchBrands();
  }, [brandSearch]);

  useEffect(() => {
    async function fetchModels() {
      if (selectedBrandId) {
        try {
          const response = await axios.get(`/api/cars/brands/${selectedBrandId}/models`, {
            params: { search: modelSearch, sort_by: 'score' }
          });
          setModels(response.data);
        } catch (error) {
          console.error('Error fetching car models:', error);
        }
      }
    }

    fetchModels();
  }, [selectedBrandId, modelSearch]);

  useEffect(() => {
    async function fetchGens() {
      if (selectedModelId && selectedBrandId) {
        try {
          const response = await axios.get(`/api/cars/brands/${selectedBrandId}/models/${selectedModelId}/gens`, {
            params: { search: genSearch, sort_by: 'score' }
          });
          setGens(response.data);
        } catch (error) {
          console.error('Error fetching car generations:', error);
        }
      }
    }

    fetchGens();
  }, [selectedModelId, selectedBrandId, genSearch]);

   useEffect(() => {
    async function fetchCategories() {
      try {
        const response = await axios.get('/api/details/categories', {
          params: { search: categorySearch, sort_by: 'score' }
        });
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching detail categories:', error);
      }
    }

    fetchCategories();
  }, [categorySearch]);

  useEffect(() => {
    async function fetchTypes() {
      if (selectedCategoryId) {
        try {
          const response = await axios.get(`/api/details/categories/${selectedCategoryId}/types`, {
            params: { search: typeSearch, sort_by: 'score' }
          });
          setTypes(response.data);
        } catch (error) {
          console.error('Error fetching detail types:', error);
        }
      }
    }

    fetchTypes();
  }, [selectedCategoryId, typeSearch]);

  const handleBrandInputChange = (e) => {
    setBrandSearch(e.target.value);
    setModels([]);
    setModelSearch('');
    setSelectedModelId('');
    setGens([]);
    setGenSearch('');
    setSelectedGenId('');

    const selectedBrand = brands.find((brand) => brand.brand_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedBrandId(selectedBrand ? selectedBrand.id : '');
  };

  const handleModelInputChange = (e) => {
    setModelSearch(e.target.value);
    setGens([]);
    setGenSearch('');
    setSelectedGenId('');

    const selectedModel = models.find((model) => model.model_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedModelId(selectedModel ? selectedModel.id : '');
  };

  const handleGenInputChange = (e) => {
    setGenSearch(e.target.value);

    const selectedGen = gens.find((gen) => gen.gen_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedGenId(selectedGen ? selectedGen.id : '');
  };

  const handleCategoryInputChange = (e) => {
    setCategorySearch(e.target.value);
    setTypes([]);
    setTypeSearch('');
    setSelectedTypeId('');

    const selectedCategory = categories.find((category) => category.category_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedCategoryId(selectedCategory ? selectedCategory.id : '');
  };

  const handleTypeInputChange = (e) => {
    setTypeSearch(e.target.value);

    const selectedType = types.find((type) => type.type_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedTypeId(selectedType ? selectedType.id : '');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
		try {
			let params = {}
			if (selectedGenId) {
				params.car_gen_id = selectedGenId
			}
			if (selectedTypeId) {
				params.detail_type_id = selectedTypeId
			}
			const response = await axios.get('/api/products', {
				params: params
			});

			console.log("searchResult:", response.data)

			setSearchResults(response.data);
		} catch (error) {
			console.error('Error searching products:', error);
		}
  };

  function CreateProductButton({auth}) {
		if (auth == null) {
			return null
		}
		return (
			<button className="create-product-button" onClick={() => {setProductModalActive(true)}}>Создать объявление</button>
		)
	}

  return (
  	<div>
  		<main>
				<div className="search-container">
					<div className="search-header">
						<form className="search-form" onSubmit={handleSubmit}>
							<div className="search-form-row">
								<input className="search-input" type="text" placeholder="Марка автомобиля" value={brandSearch} onChange={handleBrandInputChange} list="brandsList" />
								<datalist className="search-input" id="brandsList">
									{brands.map((brand) => (
										<option key={brand.id} value={brand.brand_name}>
											{brand.brand_name}
										</option>
									))}
								</datalist>
							</div>

							<div className="search-form-row">
								<input className="search-input" type="text" placeholder="Модель автомобиля" value={modelSearch} onChange={handleModelInputChange} list="modelsList" />
								<datalist className="search-input" id="modelsList">
									{models.map((model) => (
										<option key={model.id} value={model.model_name}>
											{model.model_name}
										</option>
									))}
								</datalist>
							</div>

							<div className="search-form-row">
								<input className="search-input" type="text" placeholder="Поколение автомобиля" value={genSearch} onChange={handleGenInputChange} list="gensList" />
								<datalist className="search-input" id="gensList">
									{gens.map((gen) => (
										<option key={gen.id} value={gen.gen_name}>
											{gen.gen_name}
										</option>
									))}
								</datalist>
							</div>

							<div className="search-form-row">
								<input className="search-input" type="text" placeholder="Категория детали" value={categorySearch} onChange={handleCategoryInputChange} list="categoriesList" />
								<datalist className="search-input" id="categoriesList">
									{categories.map((category) => (
										<option key={category.id} value={category.category_name}>
											{category.category_name}
										</option>
									))}
								</datalist>
							</div>

							<div className="search-form-row">
								<input className="search-input" type="text" placeholder="Тип детали" value={typeSearch} onChange={handleTypeInputChange} list="typesList" />
								<datalist className="search-input" id="typesList">
									{types.map((type) => (
										<option key={type.id} value={type.type_name}>
											{type.type_name}
										</option>
									))}
								</datalist>
							</div>
							<button className="search-button" type="submit">Искать</button>
							<AuthButton setAuthModalActive={setAuthModalActive}/>
						</form>
					</div>

					<div className="search-results-container">
						{searchResults.map((result) => (
							<div className="search-result-item">
								<div className="flex-row">
									<img className="search-result-image"
										src={result.image || 'product_photo_placeholder.png'}
									/>
									<div className="search-result-info">
										<div className="search-result-item-price">{result.price}</div>
										<div className="search-result-item-description">{result.description.slice(0, 480) + (result.description.length > 480 ? "..." : "")}</div>
									</div>
								</div>
								<div className="flex-row flex-space-between">
									<div className="mark">{result.condition === "new" ? "Новая" : "Б/у"}</div>
									<button className="search-result-item-details-button" onClick={() => {
										setSelectedProduct(result);
  									setProductModalActive(true);
									}}>
										Подробнее
									</button>
								</div>
							</div>
						))}
					</div>
				</div>
				<CreateProductButton auth={auth}/>
			</main>
			<ProductModal active={productModalActive} setActive={setProductModalActive} selectedProduct={selectedProduct} setSelectedProduct={setSelectedProduct}/>
			<AuthModal active={authModalActive} setActive={setAuthModalActive}/>
			<CreateProductModal active={createProductModalActive} setCreateProductModalActive={setCreateProductModalActive}/>
    </div>
  );
}
