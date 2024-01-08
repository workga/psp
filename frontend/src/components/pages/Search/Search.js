import React, { useState, useEffect, useContext } from 'react';
import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import './Search.css';
import { ProductModal, CreateProductModal } from "./ProductModal.js"
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
			<button className="create-product-button" onClick={() => {setCreateProductModalActive(true)}}>Создать объявление</button>
		)
	}

  return (
  	<div>
  		<main>
				<div className="search-container">
					<div className="search-header">
						<form className="search-form" onSubmit={handleSubmit}>
							{SelectorMarkupGetter()}
							<button className="search-button" type="submit" onClick={() => {setShowProfileProducts(false)}}>Искать</button>
							<AuthButton setAuthModalActive={setAuthModalActive}/>
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
			<CreateProductModal active={createProductModalActive} setActive={setCreateProductModalActive}/>
    </div>
  );
}
