import "./ProductModal.css"
import "./Search.css"
import axios from 'axios';
import React, { useState, useEffect, useContext } from 'react';

function ProductDetails({selectedProduct}) {
	if (selectedProduct == null) {
		return null
	}
	return (
		<div className="product-details">
			<div className="flex-row">
				<img className="product-image"
					src={selectedProduct.image || 'product_photo_placeholder.png'}
				/>
				<div className="search-result-info">
					<div className="product-price">{selectedProduct.price}</div>
					<div className="product-description">
						Brand: {selectedProduct.car_info.brand_name}
						<br/>
						Model: {selectedProduct.car_info.model_name}
						<br/>
						Generation: {selectedProduct.car_info.gen_name}
						<br/>
						Category: {selectedProduct.detail_info.category_name}
						<br/>
						Type: {selectedProduct.detail_info.type_name}
						<br/>
						<br/>
						{selectedProduct.description}
					</div>
				</div>
			</div>
			<div className="product-details-bottom">
				<div className="mark product-details-mark">{selectedProduct.condition === "new" ? "Новая" : "Б/у"}</div>
				<div className="mark product-details-mark">{selectedProduct.address}</div>
				<div className="mark product-details-mark">{selectedProduct.phone}</div>
			</div>
		</div>
	)
}

export function ProductModal({active, setActive, selectedProduct, setSelectedProduct}) {
	function activeModifier(className) {
		if (active) {
			className += " active"
		}
		return className
	}

	return (
		<div className={activeModifier("product-modal")} onClick={() => {
			setSelectedProduct(null);
			setActive(false);
		}}>
			<div className={activeModifier("product-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<ProductDetails selectedProduct={selectedProduct}/>
			</div>
		</div>
	);
}



function CreateProduct({setActive}) {
	const [price, setPrice] = useState(null);
	const [address, setAddress] = useState(null);
	const [condition, setCondition] = useState(null);
	const [description, setDescription] = useState(null);

	const handleCreateProduct = async (e) => {
		e.preventDefault();
		console.log(condition)
		let valid_condition = null
		if (condition == "Новая") {
			valid_condition = "new";
		}
		else if (condition == "Б/у") {
			valid_condition = "used";
		}
		else {
			console.error('Wrong condition');
			return null;
		}

		const createProductData = {
			price: price,
			address: address,
			condition: valid_condition,
			description: description,
			car_gen_id: 1,
			detail_type_id: 1
		}

		try {
				await axios.post('/api/profile/products',
						JSON.stringify(createProductData),
						{
								headers: { 'Content-Type': 'application/json' },
								withCredentials: true
						}
				);
//				setLogin('');
				setActive(false);
		} catch (err) {
			console.error('Error create product:', err);
		}
	}

	return (
		<div className="create-product">
			<form className="create-product-form" onSubmit={handleCreateProduct}>
				<div className="create-product-title">
				Создать объявление
				</div>
				<div className="flex-row full-width">
					<img className="product-image" src={'product_photo_placeholder.png'}/>
					<div className="create-product-base-info">
						<input
							className="create-product-input"
							type="text"
							placeholder="Цена"
							onChange={(e) => setPrice(e.target.value)}
							value={price}
							required
						/>
						<input
							className="create-product-input create-product-input-large"
							type="text"
							placeholder="Описание (опционально)"
							onChange={(e) => setDescription(e.target.value)}
							value={description}
						/>
					</div>
				</div>
				<div className="flex-row full-width">
						<input
							className="create-product-input"
							type="text"
							list="conditions"
							placeholder="Состояние"
							onChange={(e) => setCondition(e.target.value)}
							value={condition}
							required
						/>
						<datalist id="conditions">
							<option>Новая</option>
							<option>Б/у</option>
						</datalist>
				</div>
				<div className="flex-row full-width">
					<input
						className="create-product-input"
						type="text"
						placeholder="Адрес"
						onChange={(e) => setAddress(e.target.value)}
						value={address}
						required
					/>
				</div>
				<div className="create-product-details-bottom">
					<button className="search-result-item-details-button" onClick={(e) => {handleCreateProduct(e)}}>Создать</button>
				</div>
			</form>
		</div>
	)
}



export function CreateProductModal({active, setActive}) {
	function activeModifier(className) {
		if (active) {
			className += " active"
		}
		return className
	}

	return (
		<div className={activeModifier("product-modal")} onClick={() => {setActive(false)}}>
			<div className={activeModifier("product-modal-content create-product-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<CreateProduct setActive={setActive}/>
			</div>
		</div>
	);
}