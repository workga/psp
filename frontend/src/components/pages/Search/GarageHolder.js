import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import "./GarageHolder.css"
import { AuthContext } from "./../../../context/AuthProvider.js"
import React, { useContext, useState, useEffect } from 'react';
import { getGarage } from "./../../common/Auth.js"

export function GarageHolder() {
	const { auth, setAuth } = useContext(AuthContext);
	const name = "-search-header"

	const [selectedBrandId, setSelectedBrandId] = useLocalStorage("selectedBrandId"+name, '');
	const [selectedModelId, setSelectedModelId] = useLocalStorage("selectedModelId"+name, '');
	const [selectedGenId, setSelectedGenId] = useLocalStorage("selectedGenId"+name, '');
  const [brandSearch, setBrandSearch] = useLocalStorage("brandSearch"+name, '');
  const [modelSearch, setModelSearch] = useLocalStorage("modelSearch"+name, '');
  const [genSearch, setGenSearch] = useLocalStorage("genSearch"+name, '');

	const [garage, setGarage] = useLocalStorage("garage", null);
	const [carIndexFromGarage, setCarIndexFromGarage] = useState(-1);

	useEffect(() => {
		let carInfo = null
		if (carIndexFromGarage !== -1) {
			carInfo = garage[carIndexFromGarage]
		}
		console.log(carIndexFromGarage)
		setSelectedBrandId(carInfo?.brand_id || '');
		setSelectedModelId(carInfo?.model_id || '');
		setSelectedGenId(carInfo?.gen_id || '');
		setBrandSearch(carInfo?.brand_name || '');
		setModelSearch(carInfo?.model_name || '');
		setGenSearch(carInfo?.gen_name || '');
  }, [carIndexFromGarage]);

	async function handleAddCarToGarage() {
		if (selectedGenId) {
			try {
				await axios.post('/api/profile/garage/cars',
						JSON.stringify({car_gen_id: selectedGenId}),
						{
							headers: { 'Content-Type': 'application/json' },
							withCredentials: true
						}
				);
			} catch (error) {
        console.error('Error add car to garage:', error);
      }
			setGarage(await getGarage())
		}
	}

	async function handleDeleteCarFromGarage() {
		if (selectedGenId) {
			try {
				await axios.delete('/api/profile/garage/cars/'+selectedGenId,
						{
							withCredentials: true
						}
				);
			} catch (error) {
        console.error('Error delete car from garage:', error);
      }
			setGarage(await getGarage())
		}
	}

	return (
		<div className="garage-holder">
			{ auth && garage ?
				<select className="garage-list" value="Гараж" onChange={(e) => setCarIndexFromGarage(e.target.value)}>
					<option value={-1}>Гараж</option>
					{garage.map((car, i) => (
							<option value={i}>{car.brand_name + " >> " + car.model_name + " >> " + car.gen_name}</option>
					))}
				</select>
			: null }
			{ auth && selectedGenId && garage && !garage.find(car => car.gen_id === selectedGenId) ?
				<button className="add-car-to-garage-button" type="button" onClick={handleAddCarToGarage}>+</button>
			: null }
			{ auth && selectedGenId && garage && garage.find(car => car.gen_id === selectedGenId) ?
				<button className="add-car-to-garage-button red" type="button" onClick={handleDeleteCarFromGarage}>x</button>
			: null }
		</div>
	)
}