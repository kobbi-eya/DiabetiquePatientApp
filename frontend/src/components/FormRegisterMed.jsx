import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import registmedImage from './registmed.png';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const FormRegisterMed = () => {
  const [medecin, setMedecin] = useState({
    nom: '',
    prenom: '',
    specialite: '',
    mobile: '',
    email: '',
    date_de_naissance: new Date(),
  });
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
// Supprimer le temps et les millisecondes de la date

  const handleInputChange = (e) => {
    setMedecin({ ...medecin, [e.target.name]: e.target.value });
  };

  const handleDateChange = (date) => {
    const dateSansHeure = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    setMedecin({ ...medecin, date_de_naissance:dateSansHeure });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const dateFormatted = `${medecin.date_de_naissance.getFullYear()}-${(medecin.date_de_naissance.getMonth() + 1).toString().padStart(2, '0')}-${medecin.date_de_naissance.getDate().toString().padStart(2, '0')}`;
      const response = await api.post('/api/user/register/', {
        nom: medecin.nom,
        prenom: medecin.prenom,
        specialite: medecin.specialite,
        mobile: medecin.mobile,
        email: medecin.email,
        date_de_naissance:dateFormatted, // Utilisez medecin.date_de_naissance directement
        password: password,
        confirm_password: confirmPassword,
      });
      console.log('Valeur de success :', response.data.success);
      if (response.data.success) {
        navigate('/login');
      } else {
        console.error("L'inscription a échoué.");
      }
    } catch (error) {
      console.error("Erreur lors de l'inscription :", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <nav>
        <button className="menu-toggle" onClick={() => setIsMenuOpen(!isMenuOpen)}>
          Menu
        </button>
        <ul className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
          <li>Accueil</li>
          <li>Patients</li>
          <li>Consultations</li>
          <li>Déconnexion</li>
        </ul>
      </nav>

      <h1 className="title_medecin">Informations du médecin</h1>
      <img src={registmedImage} alt="registmed" className="registmed" />

      <div className="sous_container">
        <form onSubmit={handleSubmit}>
          <div className="format">
            <div className="left">
              <label>
                Nom:
                <input
                  type="text"
                  id="nom"
                  name="nom"
                  value={medecin.nom}
                  onChange={handleInputChange}
                />
              </label>
              <label>
                Prénom:
                <input
                  type="text"
                  id="prenom"
                  name="prenom"
                  value={medecin.prenom}
                  onChange={handleInputChange}
                />
              </label>
              <label>
                Date de naissance:
                <DatePicker
                  selected={medecin.date_de_naissance}
                  onChange={handleDateChange}
                  dateFormat="yyyy-MM-dd" // Format de la date
                  id="date_de_naissance"
                />
              </label>
              <label>
                Mobile:
                <input
                  type="tel"
                  id="mobile"
                  name="mobile"
                  value={medecin.mobile}
                  onChange={handleInputChange}
                />
              </label>
            </div>
            <div className="right">
              <label>
                Spécialiste:
                <input
                  type="text"
                  id="specialite"
                  name="specialite"
                  value={medecin.specialite}
                  onChange={handleInputChange}
                />
              </label>
              <label>
                Email:
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={medecin.email}
                  onChange={handleInputChange}
                />
              </label>
              <div>
                <label htmlFor="password">
                  Mot de passe:
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                  />
                </label>
              </div>
              <div>
                <label htmlFor="confirmPassword">
                  Confirmer mot de passe:
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                  />
                </label>
              </div>
              <button type="submit" className="confirm-button">
                Confirmer
              </button>
              <button className="cancel-button">Annuler</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FormRegisterMed;
