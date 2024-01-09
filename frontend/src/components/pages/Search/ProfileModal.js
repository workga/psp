import { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocalStorage } from "@uidotdev/usehooks";
import "./ProfileModal.css"

function ProfileDetails({setActive}) {
	const [profileInfo, setProfileInfo] = useLocalStorage("profile-info", null);

	const handleUpdateProfile = async (e) => {
		e.preventDefault();

		const updateProfileData = {
			name: profileInfo?.name,
			phone: profileInfo?.phone,
			city: profileInfo?.city,
		}

		try {
			await axios.patch('/api/profile',
				JSON.stringify(updateProfileData),
				{
						headers: { 'Content-Type': 'application/json' },
						withCredentials: true
				}
			);
			setActive(false);
		} catch (err) {
			console.error('Error update profile:', err);
		}
	}

	function setProfileInfoField(key, value) {
		let newProfileInfo = Object.assign({}, profileInfo)
		newProfileInfo[key] = value
		setProfileInfo(newProfileInfo)
	}

	return (
		<div className="profile-details">
			<div className="profile-details-title">
				Мой профиль
			</div>
			<form className="profile-form" onSubmit={handleUpdateProfile}>
				<input
					className="profile-input"
					type="text"
					placeholder="Имя"
					onChange={(e) => setProfileInfoField("name", e.target.value)}
					value={profileInfo?.name}
				/>
				<div className="profile-input gray">
					{profileInfo?.email}
				</div>
				<input
					className="profile-input"
					type="text"
					placeholder="Телефон"
					onChange={(e) => setProfileInfoField("phone", e.target.value)}
					value={profileInfo?.phone}
				/>
				<input
					className="profile-input"
					type="text"
					placeholder="Город"
					onChange={(e) => setProfileInfoField("city", e.target.value)}
					value={profileInfo?.city}
				/>
				<button className="update-profile-button" type="submit">Обновить</button>
			</form>
		</div>
	)
}


export function ProfileModal({active, setActive}) {
	function activeModifier(className) {
		if (active) {
			className += " active"
		}
		return className
	}

	return (
		<div className={activeModifier("profile-modal")} onClick={() => {
			setActive(false);
		}}>
			<div className={activeModifier("profile-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<ProfileDetails setActive={setActive}/>
			</div>
		</div>
	);
}