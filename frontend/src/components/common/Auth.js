import "./Auth.css"
import { AuthContext } from "./../../context/AuthProvider";
import { useState, useContext } from 'react';
import axios from 'axios';
import { useLocalStorage } from "@uidotdev/usehooks";


export function ProfileButton({setProfileDetailsModalActive}) {
	const { auth, setAuth } = useContext(AuthContext);
	const [profileMenuActive, setProfileMenuActive] = useState(false);
	const [searchResults, setSearchResults] = useLocalStorage("search-results", []);
	const [showProfileProducts, setShowProfileProducts] = useLocalStorage("show-profile-products", false);
	const [profileInfo, setProfileInfo] = useLocalStorage("profile-info", null);

	const [garage, setGarage] = useLocalStorage("garage", null);

	async function handleProfile() {
		setProfileMenuActive(false);
		const response = await axios.get('/api/profile', { withCredentials: true });
		setProfileInfo(response.data);
		setProfileDetailsModalActive(true);
	}


	async function handleProfileProducts() {
		setProfileMenuActive(false);
		const response = await axios.get('/api/profile/products', { withCredentials: true });
		setSearchResults(response.data);
		setShowProfileProducts(true);
	}

	async function handleLogout() {
		setProfileMenuActive(false);
		if (showProfileProducts) {
			setSearchResults([]);
			setShowProfileProducts(false);
		}
		await axios.post('/api/auth/logout', { withCredentials: true });
		setAuth(null);
		setGarage(null);
	}

	if (profileMenuActive) {
		return (
			<div className="profile-menu" onClick={(e) => {e.stopPropagation()}}>
				<button className="profile-button" type="button" onClick={() => {setProfileMenuActive(false)}}>Профиль</button>
				<button className="profile-button white" type="button" onClick={handleProfile}>Мой профиль</button>
				<button className="profile-button white" type="button" onClick={handleProfileProducts}>Мои объявления</button>
				<button className="profile-button white" type="button" onClick={handleLogout}>Выйти</button>
			</div>
		)
	}

	return (
		<button className="profile-button" type="button" onClick={() => {setProfileMenuActive(true)}}>Профиль</button>
	)
}

export function AuthButton({setAuthModalActive, setProfileDetailsModalActive}) {
	const { auth, setAuth } = useContext(AuthContext);
	if (auth == null) {
		return (
			<button className="profile-button" type="button" onClick={() => { setAuthModalActive(true) }}>Войти</button>
		)
	}

	async function handleLogout() {
		await axios.post('/api/auth/logout', { withCredentials: true });
		setAuth(null);
	}
	return (
		<ProfileButton setProfileDetailsModalActive={setProfileDetailsModalActive}/>
	)
}

export async function getGarage() {
	try {
		const response = await axios.get('/api/profile/garage',
			{
				withCredentials: true
			}
		);
		return response.data;
	} catch (error) {
		console.error('Error get garage:', error);
		return [];
	}
}

function Auth({setActive, registerMenuActive, setRegisterMenuActive}) {
	const { auth, setAuth } = useContext(AuthContext);
	const [name, setName] = useState('buba');  // REPLACE BY ''
	const [login, setLogin] = useState('testing0@example.com');  // REPLACE BY ''
	const [pwd, setPwd] = useState('testing_profile'); // REPLACE BY ''
	const [phone, setPhone] = useState('79009009000');  // REPLACE BY ''
	const [city, setCity] = useState('Vegas');  // REPLACE BY ''

	const [garage, setGarage] = useLocalStorage("garage", null);

	const handleLogin = async (e) => {
		e.preventDefault();

		const authData = {
			email: login,
			password: pwd
		}

		try {
				await axios.post('/api/auth/login',
						JSON.stringify(authData),
						{
								headers: { 'Content-Type': 'application/json' },
								withCredentials: true
						}
				);
				const profileInfo = await axios.get('/api/profile',
						{ withCredentials: true }
				);
				setAuth(profileInfo);
				setGarage(await getGarage())
				setLogin('testing0@example.com');  // REPLACE BY ''
				setPwd('testing_profile'); // REPLACE BY ''
				setActive(false);
		} catch (err) {
			console.error('Error login:', err);
		}
	}

	const handleRegister = async (e) => {
		e.preventDefault();

		const registerData = {
			email: login,
			password: pwd,
			name: name,
			phone: phone,
			city: city,
		}

		try {
				await axios.post('/api/auth/register',
						JSON.stringify(registerData),
						{
								headers: { 'Content-Type': 'application/json' },
								withCredentials: true
						}
				);
				setActive(false);
				setRegisterMenuActive(false)
		} catch (err) {
			console.error('Error register:', err);
		}
	}

	if (registerMenuActive) {
		return (
			<div className="auth auth-register">
				<div className="auth-title">
				Регистрация
				</div>
				<form className="auth-form" onSubmit={handleLogin}>
					<input
						className="auth-input"
						type="text"
						placeholder="Имя"
						onChange={(e) => setName(e.target.value)}
						value={name}
						required
					/>
					<input
						className="auth-input"
						type="text"
						placeholder="Email"
						onChange={(e) => setLogin(e.target.value)}
						value={login}
						required
					/>
					<input
						className="auth-input"
						type="password"
						placeholder="Пароль"
						onChange={(e) => setPwd(e.target.value)}
						value={pwd}
						required
					/>
					<input
						className="auth-input"
						type="text"
						placeholder="Телефон"
						onChange={(e) => setPhone(e.target.value)}
						value={phone}
						required
					/>
					<input
						className="auth-input"
						type="text"
						placeholder="Город"
						onChange={(e) => setCity(e.target.value)}
						value={city}
						required
					/>
					<div className="auth-buttons">
						<button className="sign-in-button" type="submit" onClick={() => {setRegisterMenuActive(false)}}>Назад</button>
						<button className="sign-in-button sign-up-button" type="button" onClick={(e) => {handleRegister(e)}}>Зарегистрироваться</button>
					</div>
				</form>
			</div>
		)
	}
	return (
		<div className="auth">
			<div className="auth-title">
			Войти в профиль
			</div>
			<form className="auth-form" onSubmit={handleLogin}>
				<input
					className="auth-input"
					type="text"
					placeholder="Email"
					onChange={(e) => setLogin(e.target.value)}
					value={login}
					required
				/>
				<input
					className="auth-input"
					type="password"
					placeholder="Пароль"
					onChange={(e) => setPwd(e.target.value)}
					value={pwd}
					required
				/>
				<div className="auth-buttons">
					<button className="sign-in-button" type="submit">Войти</button>
					<button className="sign-in-button sign-up-button" type="button" onClick={() => {setRegisterMenuActive(true)}}>Регистрация</button>
				</div>
			</form>
		</div>
	)
}

export function AuthModal({active, setActive}) {
	const [registerMenuActive, setRegisterMenuActive] = useState(false);

	function activeModifier(className) {
		if (active) {
			className += " active"
		}
		return className
	}

	return (
		<div className={activeModifier("auth-modal")} onClick={() => {
			setActive(false);
			setRegisterMenuActive(false)
		}}>
			<div className={activeModifier("auth-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<Auth setActive={setActive} registerMenuActive={registerMenuActive} setRegisterMenuActive={setRegisterMenuActive}/>
			</div>
		</div>
	);
}