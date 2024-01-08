import "./Auth.css"
import { AuthContext } from "./../../context/AuthProvider";
import { useState, useContext } from 'react';
import axios from 'axios';
import { useLocalStorage } from "@uidotdev/usehooks";


export function ProfileButton() {
	const { auth, setAuth } = useContext(AuthContext);
	const [profileMenuActive, setProfileMenuActive] = useState(false);
	const [searchResults, setSearchResults] = useLocalStorage("search-results", []);
	const [showProfileProducts, setShowProfileProducts] = useLocalStorage("show-profile-products", false);


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
	}

	if (profileMenuActive) {
		return (
			<div className="profile-menu" onClick={(e) => {e.stopPropagation()}}>
				<button className="profile-button" type="button" onClick={() => {setProfileMenuActive(false)}}>Профиль</button>
				<button className="profile-button white" type="button" onClick={handleProfileProducts}>Мои объявления</button>
				<button className="profile-button white" type="button" onClick={handleLogout}>Выйти</button>
			</div>
		)
	}

	return (
		<button className="profile-button" type="button" onClick={() => {setProfileMenuActive(true)}}>Профиль</button>
	)
}

export function AuthButton({setAuthModalActive}) {
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
		<ProfileButton/>
	)
}

function Auth({setActive}) {
	const { auth, setAuth } = useContext(AuthContext);
	const [login, setLogin] = useState('testing0@example.com');  // REPLACE BY ''
	const [pwd, setPwd] = useState('testing_profile'); // REPLACE BY ''

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
				setLogin('testing0@example.com');  // REPLACE BY ''
				setPwd('testing_profile'); // REPLACE BY ''
				setActive(false);
		} catch (err) {
			console.error('Error login:', err);
		}
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
					<button className="sign-in-button sign-up-button" type="button">Зарегистрироваться</button>
				</div>
			</form>
		</div>
	)
}

export function AuthModal({active, setActive}) {
	function activeModifier(className) {
		if (active) {
			className += " active"
		}
		return className
	}

	return (
		<div className={activeModifier("auth-modal")} onClick={() => {
			setActive(false);
		}}>
			<div className={activeModifier("auth-modal-content")} onClick={(e) => {e.stopPropagation()}}>
				<Auth setActive={setActive}/>
			</div>
		</div>
	);
}