import "./ProductModal.css"
import "./Search.css"

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



function CreateProduct() {
	return (
		<div>
			keka
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
		<div className={activeModifier("product-modal")} onClick={() => {
			setActive(false);
		}}>
			<div className={activeModifier("product-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<CreateProduct/>
			</div>
		</div>
	);
}