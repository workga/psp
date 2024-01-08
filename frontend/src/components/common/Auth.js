import "./Auth.css"
import { AuthContext } from "./../../context/AuthProvider";
import { useRef, useState, useEffect, useContext } from 'react';
import axios from 'axios';

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
		<button className="profile-button" type="button" onClick={handleLogout}>Выйти</button>
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