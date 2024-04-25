/*import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import '../styles/Patient.css';
import patientImage from "./patients.png";
import consultImage from "./consult1.png";
import { useNavigate } from "react-router-dom";
//import deleteIcon from "./deleteicon.png"
function Listepatient() {
  const [patientsData, setPatientsData] = useState([]);
  const [showPatients, setShowPatients] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const { medecinId } = useParams();
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();
  const [patientToDelete, setPatientToDelete] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleShowPatients = () => {
    api.get(`http://localhost:8000/api/medecin/ListesPatients/${medecinId}/`)
      .then((res) => {
        setPatientsData(res.data.patients);
        setShowPatients(true);
      })
      .catch((error) => {
        console.error('Error fetching patients:', error);
      });
  };

  /*const handleGetPatientInfo = (patientId) => {
    api.get(`http://localhost:8000/api/patients/${patientId}`)
      .then((res) => {
        setSelectedPatient(res.data);
      })
      .catch((error) => {
        console.error('Error fetching patient information:', error);
      });
  };*/

  const handleDeletePatient = (patientId) => {
    setPatientsData(patientsData.filter(patient => patient.id !== patientId));
    // Cacher l'icône de confirmation après la suppression
    setShowConfirmation(false);
  };

 /* const confirmDeletion = (patientId) => {
    // Afficher la page de confirmation et définir le patient à supprimer
    setPatientToDelete(patientId);
  };*/
/*
  useEffect(() => {
    handleShowPatients();
  }, []);

  return (
    <div className="container">
      <button className="list_patients_button" onClick={handleShowPatients}>
        Liste des Patients
      </button>
      {showPatients && (
        <div className="format">
          <h1 className="title_patients">Liste des patients</h1>
          <div className="right">
            <img src={consultImage} alt="consult" className="consult" />
          </div>
          <div className="left">
            <img src={patientImage} alt="patient" className="patient" />
            <div className="table-container">
              <div className="search-container">
                <input
                  type="text"
                  placeholder="Rechercher"
                  value={searchTerm}
                  onChange={(event) => setSearchTerm(event.target.value)}
                />
                <button className="clean-button">Nettoyer</button>
                <button className="ajout-button" onClick={() =>navigate(`/login/registerpatient/${medecinId}`)}>Ajouter un patient</button>

                {/* Ajouter ici le bouton pour ajouter un patient }*/
       /*       </div>
              <table>
                <thead>
                  <tr>
                    <th>Nom</th>
                    <th>Prénom</th>
                    <th>Date de Naissance</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {patientsData.map((patient) => (
                    <tr key={patient.id}>
                      <td>{patient.nom}</td>
                      <td>{patient.prenom}</td>
                      <td>{patient.date_de_naissance}</td>
                      <td>
                        <button onClick={() => navigate(`/ListePatient/Info/${patient.id}`)}>Information</button>
                        <button onClick={() => handleDeletePatient(patient.id)}>Supprimer</button>

                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
      {selectedPatient && (
        <div className="right">
          <h2>Informations du Patient</h2>
          <p>Nom: {selectedPatient.nom}</p>
          <p>Prénom: {selectedPatient.prenom}</p>
          {/* Afficher d'autres informations du patient ici }*/
    /*    </div>
      )}
    </div>
  );
}

export default Listepatient;*/

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import '../styles/Patient.css';
import patientImage from "./patients.png";
import consultImage from "./consult1.png";
import supprimerImage from "./supprimer.png";
import { useNavigate } from "react-router-dom";
//import deleteIcon from "./deleteicon.png";

function Listepatient() {
  const [patientsData, setPatientsData] = useState([]);
  const [showPatients, setShowPatients] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const { medecinId } = useParams();
  const navigate = useNavigate();
  const [sortBy, setSortBy] = useState("nom");
  const [sortOrder, setSortOrder] = useState("asc");
  const [searchTerm, setSearchTerm] = useState("");
  const [sortAge, setSortAge] = useState("asc");
  const [patientIdToDelete, setPatientIdToDelete] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleShowPatients = () => {
    api.get(`http://localhost:8000/api/medecin/ListesPatients/${medecinId}/`)
      .then((res) => {
        setPatientsData(res.data.patients);
        setShowPatients(true);
      })
      .catch((error) => {
        console.error('Error fetching patients:', error);
      });
  };

  const handleGetPatientInfo = (patientId) => {
    api.get(`http://localhost:8000/api/patients/${patientId}`)
      .then((res) => {
        setSelectedPatient(res.data);
      })
      .catch((error) => {
        console.error('Error fetching patient information:', error);
      });
  };

  const handleDeletePatient = (patientId) => {
    setPatientsData(patientsData.filter(patient => patient.id !== patientId));
    // Cacher l'icône de confirmation après la suppression
    setShowConfirmation(false);
  };
  

  const confirmDeletion = (patientId) => {
    // Afficher la page de confirmation et définir le patient à supprimer
    setPatientIdToDelete(patientId);
    setShowConfirmation(true);
  };

  useEffect(() => {
    handleShowPatients();
    handleDeletePatient ();
  }, []);

  const filteredPatientsData = patientsData.filter((patient) => {
    return (
      patient.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.prenom.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const sortedPatientsData = filteredPatientsData.sort((a, b) => {
    if (sortBy === "nom" || sortBy === "prenom") {
      const nameA = a[sortBy].toUpperCase();
      const nameB = b[sortBy].toUpperCase();
      if (nameA < nameB) {
        return sortOrder === "asc" ? -1 : 1;
      }
      if (nameA > nameB) {
        return sortOrder === "asc" ? 1 : -1;
      }
      return 0;
    }
    if (sortBy === "age") {
      return sortOrder === "asc" ? a.age - b.age : b.age - a.age;
    }
    return 0;
  });

  const toggleSortOrder = (sortByField) => {
    if (sortBy === sortByField) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortOrder("asc");
    }
    setSortBy(sortByField);
  };

  return (
    <div className="container">
      <button className="list_patients_button" onClick={handleShowPatients}>
        Liste des Patients
      </button>
      {showPatients && (
        <div className="format">
          <h1 className="title_patients">Liste des patients</h1>
          <div className="right">
            <img src={consultImage} alt="consult" className="consult" />
          </div>
          <div className="left">
            <img src={patientImage} alt="patient" className="patient" />
            <div className="table-container">
              <div className="search-container">
                <input
                  type="text"
                  placeholder="Rechercher"
                  value={searchTerm}
                  onChange={(event) => setSearchTerm(event.target.value)}
                />
                <button className="clean-button" onClick={() => setSearchTerm("")}>
                  Nettoyer
                </button>
                <button className="ajout-button" onClick={() => navigate(`/login/registerpatient/${medecinId}`)}>
                  Ajouter un patient
                </button>
              </div>
              <table>
                <thead>
                  <tr>
                    <th onClick={() => toggleSortOrder("nom")}>
                      Nom
                      {sortBy === "nom" && <span>{sortOrder === "asc" ? " ↑" : " ↓"}</span>}
                    </th>
                    <th onClick={() => toggleSortOrder("prenom")}>
                      Prénom
                      {sortBy === "prenom" && <span>{sortOrder === "asc" ? " ↑" : " ↓"}</span>}
                    </th>
                    <th onClick={() => toggleSortOrder("age")}>
                      Âge
                      {sortBy === "age" && <span>{sortOrder === "asc" ? " ↑" : " ↓"}</span>}
                    </th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedPatientsData.map((patient) => (
                    <tr key={patient.id}>
                      <td>{patient.nom}</td>
                      <td>{patient.prenom}</td>
                      <td>{patient.date_de_naissance}</td>
                      <td>
                        <button onClick={() => navigate(`/ListePatient/Info/${patient.id}`)}>Information</button>
                        <button onClick={() => confirmDeletion(patient.id)}>Supprimer</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
      {showConfirmation && (
        <div className="confirmation-modal">
          <img src={supprimerImage} alt="supprimer" className="supprimer" />
          <p>Êtes-vous sûr de vouloir supprimer ce patient ?</p>
          <button onClick={() =>  setPatientIdToDelete(null)}>Oui</button>

          <button onClick={() => setShowConfirmation(false)}>Non</button>
        </div>
      )}
      {selectedPatient && (
        <div className="right">
          <h2>Informations du Patient</h2>
          <p>Nom: {selectedPatient.nom}</p>
          <p>Prénom: {selectedPatient.prenom}</p>
          {/* Afficher d'autres informations du patient ici */}
        </div>
      )}
    </div>
  );
}

export default Listepatient;