import { useLocalStorage } from "@uidotdev/usehooks";
import axios from 'axios';
import "./GarageHolder.css"
import { AuthContext } from "./../../../context/AuthProvider.js"
import React, { useContext, useEffect } from 'react';
import { getGarage } from "./../../common/Auth.js"

export function GarageHolder() {
	const { auth, setAuth } = useContext(AuthContext);
	const name = "-search-header"
	const [selectedGenId, setSelectedGenId] = useLocalStorage("selectedGenId"+name, '');

	const [garage, setGarage] = useLocalStorage("garage", null);

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
	return (
		<div className="garage-holder">
			{auth && selectedGenId && garage && !garage.find(car => car.gen_id === selectedGenId) ? <button className="add-car-to-garage-button" onClick={handleAddCarToGarage}>+</button> : null }
		</div>
	)
}