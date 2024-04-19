import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/FormLogin.css";
import logo from "./logo.png";
import doctor from "./doctor.png";
import axios from "axios"; // Importez Axios
import RegisterPatient from "../pages/RegisterPatient";
function FormLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [idmed_id, setIdmed] = useState(null);
  const [loading, setLoading] = useState(false); // Ajout de loading
  const navigate = useNavigate();

       const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true); // Définir loading à true lors de la soumission du formulaire
         console.log("Email:", email);
         console.log("Password:", password);
        try {
          const res = await api.post("/api/user/login/", { email, password });
          console.log('API Response:', res.data);
          // Vérifier si la réponse contient les clés attendues
          if ('role' in res.data) {
             //localStorage.setItem(ACCESS_TOKEN, res.data.access);
             //localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
      
            // Rediriger en fonction du rôle de l'utilisateur
            if (res.data.role === 'MEDECIN') {
              navigate('/home_medecin', { state: { idmed_id: res.data.idmed_id } });
              console.log('ID du médecin:', res.data.idmed_id);
              setIdmed(res.data.idmed_id);
            
  
            } else if (res.data.role === 'PATIENT') {
              navigate('/home_patient');
            }
          } else {
            // Si la structure de la réponse est différente, afficher une erreur
            throw new Error("La structure de la réponse de l'API est incorrecte.");
          }
        } catch (error) {
          alert("Erreur lors de la connexion : " + error.message);
        } finally {
          setLoading(false); // Définir loading à false une fois le traitement terminé
        }
      };

  return (
    <div className="container">
      <div className='title_connection'>Se connecter à votre compte</div>
      <div className="sous-container">
        <div className="left">
           <img src={logo} alt="logo" className="logo" />
           <img src={doctor} alt="man" className="doctor" />
        </div>
        <div className="right">
          <form onSubmit={handleSubmit}>
            <label htmlFor="email">Nom de l'utilisateur:</label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="exemple@gmail.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
            <label htmlFor="password">Mot de passe:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
            <div className="submit">
              <button type="submit" disabled={loading}>Se connecter</button> {/* Désactiver le bouton de soumission pendant le chargement */}
            </div>
          </form>
        </div>
        
      </div>
      
    </div>
  );
}

export default FormLogin;
