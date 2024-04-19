import React, { useState } from "react";
import api from "../api";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/FormPatient.css";
import { useNavigate } from 'react-router-dom';



const FormPatient = ({medecinId}) => {
  const [patient, setPatient] = useState({
    nom: '',
    prenom: '',
    sexe: 'HOMME',
    poids: '',
    taille: '',
    mobile: '',
    allergies: '',
    groupe_sanguin: 'A+',
    date_de_naissance: new Date(),
    type_diabete: '',
    email: ''
    
  });
 // const [idmed, setIdMedecin] = useState(null);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const handlePatientInputChange = (e) => {
    setPatient({ ...patient, [e.target.name]: e.target.value });
  };

  const handleDateChange = (date) => {
    const dateSansHeure = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    setPatient({ ...patient, date_de_naissance: dateSansHeure });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
 
    
    try {
      const dateFormatted = `${patient.date_de_naissance.getFullYear()}-${(patient.date_de_naissance.getMonth() + 1).toString().padStart(2, '0')}-${patient.date_de_naissance.getDate().toString().padStart(2, '0')}`;
      console.log("Données du formulaire :", patient);
      const response = await api.post('api/user/patientReg/', {
        nom: patient.nom,
        prenom: patient.prenom,
        poids: patient.poids,
        taille: patient.taille,
        mobile: patient.mobile,
        allergies: patient.allergies,
        groupe_sanguin: patient.groupe_sanguin,
        date_de_naissance: dateFormatted,
        type_diabete: patient.type_diabete,
        email: patient.email,
        sexe: patient.sexe,
        password: password,
        confirm_password: confirmPassword,
        idmed_id: medecinId ? medecinId :0
       
        
      });
      console.log('Valeur de success :', response.data.success);
      if (response.data.success) {
        //const idmed = response.data.idmed;
        //console.log('Identifiant du médecin:', idMedecin);
        navigate('/home_medecin');
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
        
      <h1 className="title_patients">Informations du patient</h1>
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
                value={patient.nom}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Prénom:
              <input
                type="text"
                id="prenom"
                name="prenom"
                value={patient.prenom}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Sexe:
              <select
                id="sexe"
                name="sexe"
                value={patient.sexe}
                onChange={handlePatientInputChange}
              >
                <option value="HOMME">HOMME</option>
                <option value="FEMME">FEMME</option>
              </select>
              </label>
              <label>Date de naissance:
              <DatePicker
                id="date_de_naissance"
                selected={patient.date_de_naissance}
                onChange={handleDateChange}
                dateFormat="yyyy-MM-dd"
              />
              </label>
              <label>Mobile:
              <input
                type="tel"
                id="mobile"
                name="mobile"
                value={patient.mobile}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Email:
              <input
                type="email"
                id="email"
                name="email"
                value={patient.email}
                onChange={handlePatientInputChange}
              />
              </label>
            </div>
            <div className="right">
              <label>Type diabète:
              <input
                type="text"
                id="type_diabete"
                name="type_diabete"
                value={patient.type_diabete}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Allergies:
              <input
                type="text"
                id="allergies"
                name="allergies"
                value={patient.allergies}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Taille:
              <input
                type="text"
                id="taille"
                name="taille"
                value={patient.taille}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Poids:
              <input
                type="text"
                id="poids"
                name="poids"
                value={patient.poids}
                onChange={handlePatientInputChange}
              />
              </label>
              <label>Groupe sanguin:
              <select
                id="groupe_sanguin"
                name="groupe_sanguin"
                value={patient.groupe_sanguin}
                onChange={handlePatientInputChange}
              >
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
              </label>
              <div>
                <label>Mot de passe:
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
                <label >Confirmer mot de passe:
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                />
                </label>
              </div>
            </div>
          </div>
          <button type="submit" className="confirm-button">
            Confirmer
          </button>
          <button type="button" className="cancel-button">
            Annuler
          </button>
        </form>
      </div>
    </div>
  );
};

export default FormPatient;
