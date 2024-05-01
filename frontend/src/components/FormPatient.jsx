import React, { useState } from "react";
import api from "../api";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import registpatientImage from "../images/editpatient.png";
import "../styles/FormPatient.css";
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';


const FormPatient = () => {
  const { medecinId } = useParams();
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
  const [error, setError] = useState('');
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
      const response = await api.post(`api/user/patientReg/${medecinId}`, {
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
        navigate(`/login/home_medecin/${medecinId}`, { state: { idmed_id: medecinId } });
      } else {
        console.error("L'inscription a échoué.");
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error); // Affichage du message d'erreur provenant de l'API
      } else {
        console.error("Erreur lors de l'inscription :", error);
      }
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="container_registpatient">
    <h1 className="title_patients_registpatient">Informations du patient</h1>
    <img src={registpatientImage} alt="registpatient" className="editpatient_registpatient" />

    <div className="sous_container_registpatient">
      <form onSubmit={handleSubmit}>
        <div className="format_registpatient">
          <div className="left_registpatient">
            
            <label className="label_registpatient">
              Nom:
            <input className="input_registpatient"
              type="text"
              id="nom"
              name="nom"
              value={patient.nom}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Prénom:
            <input className="input_registpatient"
              type="text"
              id="prenom"
              name="prenom"
              value={patient.prenom}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Sexe:
            <select className="select_registpatient"
              id="sexe"
              name="sexe"
              value={patient.sexe}
              onChange={handlePatientInputChange}
            >
              <option className="option_registpatient"  value="HOMME">HOMME</option>
              <option className="option_registpatient" value="FEMME">FEMME</option>
            </select>
            </label>
            <label className="label_registpatient">Date de naissance:
            <DatePicker className="datepicker_registpatient"
              id="date_de_naissance"
              selected={patient.date_de_naissance}
              onChange={handleDateChange}
              dateFormat="yyyy-MM-dd"
            />
            </label>
            <label className="label_registpatient"> Mobile:
            <input className="input_registpatient"
              type="tel"
              id="mobile"
              name="mobile"
              value={patient.mobile}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Email:
            <input className="input_registpatient"
              type="email"
              id="email"
              name="email"
              value={patient.email}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Type diabète:
            <input className="input_registpatient"
              type="text"
              id="type_diabete"
              name="type_diabete"
              value={patient.type_diabete}
              onChange={handlePatientInputChange}
            />
            </label>
          </div>
          <div className="right_registpatient">
            
            <label className="label_registpatient">Allergies:
            <input className="input_registpatient"
              type="text"
              id="allergies"
              name="allergies"
              value={patient.allergies}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Taille:
            <input  className="input_registpatient"
              type="text"
              id="taille"
              name="taille"
              value={patient.taille}
              onChange={handlePatientInputChange}
            />
            </label >
            <label className="label_registpatient">Poids:
            <input className="input_registpatient"
              type="text"
              id="poids"
              name="poids"
              value={patient.poids}
              onChange={handlePatientInputChange}
            />
            </label>
            <label className="label_registpatient">Groupe sanguin:
            <select className="select_registpatient"
              id="groupe_sanguin"
              name="groupe_sanguin"
              value={patient.groupe_sanguin}
              onChange={handlePatientInputChange}
            >
              <option className="option_registpatient" value="A+">A+</option>
              <option className="option_registpatient" value="A-">A-</option>
              <option className="option_registpatient" value="B+">B+</option>
              <option className="option_registpatient" value="B-">B-</option>
              <option className="option_registpatient" value="AB+">AB+</option>
              <option className="option_registpatient" value="AB-">AB-</option>
              <option className="option_registpatient" value="O+">O+</option>
              <option className="option_registpatient" value="O-">O-</option>
            </select>
            </label>
            <div>
              <label className="label_registpatient">Mot de passe:
              <input className="input_registpatient"
                type="password"
                id="password"
                name="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              </label>
            </div>
            <div>
              <label className="label_registpatient" >Confirmer mot de passe:
              <input className="input_registpatient"
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
        <button type="submit" className="confirm-button_registpatient">
          Confirmer
        </button>
        <button type="button" className="cancel-button_registpatient">
          Annuler
        </button>
      </form>
    </div>
  </div>
);
};
export default FormPatient;