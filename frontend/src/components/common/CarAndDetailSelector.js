import React, { useState, useEffect, useContext } from 'react';
import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import "./CarAndDetailSelector.css"

export function CarAndDetailSelector({isLong, name}) {
  const [brands, setBrands] = useLocalStorage("brands"+name, []);
  const [models, setModels] = useLocalStorage("models"+name, []);
  const [gens, setGens] = useLocalStorage("gens"+name, []);
  const [categories, setCategories] = useLocalStorage("categories"+name, [])
  const [types, setTypes] = useLocalStorage("types"+name, [])

  const [selectedBrandId, setSelectedBrandId] = useLocalStorage("selectedBrandId"+name, '');
  const [selectedModelId, setSelectedModelId] = useLocalStorage("selectedModelId"+name, '');
  const [selectedGenId, setSelectedGenId] = useLocalStorage("selectedGenId"+name, '');
	const [selectedCategoryId, setSelectedCategoryId] = useLocalStorage("selectedCategoryId"+name, '');
	const [selectedTypeId, setSelectedTypeId] = useLocalStorage("selectedTypeId"+name, '');

  const [brandSearch, setBrandSearch] = useLocalStorage("brandSearch"+name, '');
  const [modelSearch, setModelSearch] = useLocalStorage("modelSearch"+name, '');
  const [genSearch, setGenSearch] = useLocalStorage("genSearch"+name, '');
	const [categorySearch, setCategorySearch] = useLocalStorage("categorySearch"+name, '');
	const [typeSearch, setTypeSearch] = useLocalStorage("typeSearch"+name, '');

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

	function SelectorMarkupGetter() {
		const selectorTypeClassName = isLong ? "selector-long" : "selector-short";
		return (
			<div className={selectorTypeClassName}>
				<div className="selector-holder">
					<div>
						<input className="search-input" type="text" placeholder="Марка автомобиля" value={brandSearch} onChange={handleBrandInputChange} list={"brandsList"+name} />
						<datalist className="search-input" id={"brandsList"+name}>
							{brands.map((brand) => (
								<option key={brand.id} value={brand.brand_name}>
									{brand.brand_name}
								</option>
							))}
						</datalist>
					</div>

					<div>
						<input className="search-input" type="text" placeholder="Модель автомобиля" value={modelSearch} onChange={handleModelInputChange} list={"modelsList"+name} />
						<datalist className="search-input" id={"modelsList"+name}>
							{models.map((model) => (
								<option key={model.id} value={model.model_name}>
									{model.model_name}
								</option>
							))}
						</datalist>
					</div>

					<div>
						<input className="search-input" type="text" placeholder="Поколение автомобиля" value={genSearch} onChange={handleGenInputChange} list={"gensList"+name} />
						<datalist className="search-input" id={"gensList"+name}>
							{gens.map((gen) => (
								<option key={gen.id} value={gen.gen_name}>
									{gen.gen_name}
								</option>
							))}
						</datalist>
					</div>
				</div>
				<div className="selector-holder">
					<div>
						<input className="search-input" type="text" placeholder="Категория детали" value={categorySearch} onChange={handleCategoryInputChange} list={"categoriesList"+name} />
						<datalist className="search-input" id={"categoriesList"+name}>
							{categories.map((category) => (
								<option key={category.id} value={category.category_name}>
									{category.category_name}
								</option>
							))}
						</datalist>
					</div>

					<div>
						<input className="search-input" type="text" placeholder="Тип детали" value={typeSearch} onChange={handleTypeInputChange} list={"typesList"+name} />
						<datalist className="search-input" id={"typesList"+name}>
							{types.map((type) => (
								<option key={type.id} value={type.type_name}>
									{type.type_name}
								</option>
							))}
						</datalist>
					</div>
				</div>
			</div>
		)
	}

	return [selectedGenId, selectedTypeId, SelectorMarkupGetter]
}