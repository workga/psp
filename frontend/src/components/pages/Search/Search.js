import React, { useState, useEffect, useContext } from 'react';
import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import './Search.css';
import { ProductModal, CreateProductModal } from "./ProductModal.js"
import { ProfileModal } from "./ProfileModal.js"
import { AuthModal, AuthButton } from "./../../common/Auth.js"
import { AuthContext } from "./../../../context/AuthProvider.js"
import { CarAndDetailSelector } from "./../../common/CarAndDetailSelector.js"

export function Search() {
	const { auth, setAuth } = useContext(AuthContext);
	const [selectedGenId, selectedTypeId, SelectorMarkupGetter] = CarAndDetailSelector({isLong:true,name:"-search-header"})

  const [searchResults, setSearchResults] = useLocalStorage("search-results", []);
  const [showProfileProducts, setShowProfileProducts] = useLocalStorage("show-profile-products", false);

  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productModalActive, setProductModalActive] = useState(false);
  const [authModalActive, setAuthModalActive] = useState(false);
  const [createProductModalActive, setCreateProductModalActive] = useState(false);
  const [profileDetailsModalActive, setProfileDetailsModalActive] = useState(false);

  const [profileInfo, setProfileInfo] = useLocalStorage("profile-info", null);

  const [minPriceFilter, setMinPriceFilter] = useLocalStorage("minPriceFilter", '');
	const [maxPriceFilter, setMaxPriceFilter] = useLocalStorage("maxPriceFilter", '');
	const [cityFilter, setCityFilter] = useLocalStorage("cityFilter", '');
	const [conditionFilter, setConditionFilter] = useLocalStorage("conditionFilter", '');
	const [sortFilter, setSortFilter] = useLocalStorage("sortFilter", '');
	const [descFilter, setDescFilter] = useLocalStorage("descFilter", '');


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
			if (minPriceFilter) {
				params.min_price = minPriceFilter
			}
			if (maxPriceFilter) {
				params.max_price = maxPriceFilter
			}
			if (cityFilter) {
				params.city = cityFilter
			}
			if (conditionFilter) {
				params.condition = conditionFilter
			}
			if (sortFilter) {
				params.sort_by = sortFilter
			}
			console.log(descFilter)
			if (descFilter) {
				params.desc = descFilter
			}

			const response = await axios.get('/api/products', {
				params: params
			});

			setSearchResults(response.data);
		} catch (error) {
			console.error('Error searching products:', error);
		}
  };

  const handleDeleteProduct = async (e, result) => {
    e.preventDefault();
		try {
			await axios.delete('/api/profile/products/'+result.id);

			let newSearchResults = searchResults.filter((item) => {return item.id !== result.id })
			setSearchResults(newSearchResults);
		} catch (error) {
			console.error('Error delete product:', error);
		}
  };

  const handleDetails = async (result) => {
		try {
			await axios.post('/api/products/'+result.id+'/increase_score');
		} catch (error) {
			console.error('Error increase product score:', error);
		}
  };

  function CreateProductButton({auth}) {
		if (auth == null) {
			return null
		}
		return (
			<button className="create-product-button" onClick={() => {setCreateProductModalActive(true)}}>Создать объявление</button>
		)
	}

  return (
  	<div>
  		<main>
				<div className="search-container">
					<div className="search-header filters-header">

						<div className="selector-holder">
							<div>
								<input
									className="search-input"
									type="text"
									placeholder="Цена от"
									value={minPriceFilter}
									onChange={(e) => {setMinPriceFilter(e.target.value)}}
								/>
							</div>
							<div>
								<input
									className="search-input"
									type="text"
									placeholder="Цена до"
									value={maxPriceFilter}
									onChange={(e) => {setMaxPriceFilter(e.target.value)}}
								/>
							</div>
							<div>
								<input
									className="search-input"
									type="text"
									placeholder="Город"
									value={cityFilter}
									onChange={(e) => {setCityFilter(e.target.value)}}
								/>
							</div>
							<div>
								<select className="search-input" value={conditionFilter} onChange={(e) => setConditionFilter(e.target.value)}>
									<option value={''}>Состояние</option>
									<option value={"new"}>Новая</option>
									<option value={"used"}>Б/у</option>
								</select>
							</div>
							<div>
								<select className="search-input" value={sortFilter} onChange={(e) => setSortFilter(e.target.value)}>
									<option value={''}>Сортировка</option>
									<option value={"time"}>Время публикации</option>
									<option value={"price"}>Цена</option>
									<option value={"score"}>Популярность</option>
								</select>
							</div>
							<div>
								<select className="search-input" value={descFilter} onChange={(e) => setDescFilter(e.target.value)}>
									<option value={''}>Сортировать по</option>
									<option value={false}>Возрастанию</option>
									<option value={true}>Убыванию</option>
								</select>
							</div>
						</div>

					</div>

					<div className="search-header">
						<form className="search-form" onSubmit={handleSubmit}>
							{SelectorMarkupGetter()}
							<button className="search-button" type="submit" onClick={() => {setShowProfileProducts(false)}}>Искать</button>
							<AuthButton setAuthModalActive={setAuthModalActive} setProfileDetailsModalActive={setProfileDetailsModalActive}/>
						</form>
					</div>

					<div className="search-results-container">
						{showProfileProducts ? <div className="products-title">Мои объявления</div> : null}
						{searchResults.map((result) => (
							<div className="search-result-item">
								<div className="flex-row">
									<img className="search-result-image"
										src={result.image || 'product_photo_placeholder.png'}
									/>
									<div className="search-result-info">
										<div className="flex-row space-between">
											<div className="search-result-item-price">{result.price}</div>
											{showProfileProducts ? <button className="search-result-item-details-button delete" onClick={(e) => {handleDeleteProduct(e, result)}}>x</button> : null}
										</div>
										<div className="search-result-item-description">{result.description.slice(0, 480) + (result.description.length > 480 ? "..." : "")}</div>
									</div>
								</div>
								<div className="flex-row flex-space-between">
									<div className="mark">{result.condition === "new" ? "Новая" : "Б/у"}</div>
									<button className="search-result-item-details-button" onClick={() => {
										setSelectedProduct(result);
  									setProductModalActive(true);
  									handleDetails(result);
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
			<CreateProductModal active={createProductModalActive} setActive={setCreateProductModalActive}/>
			<ProfileModal active={profileDetailsModalActive} setActive={setProfileDetailsModalActive}/>
    </div>
  );
}
