import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'; // Assurez-vous d'importer les styles CSS si nécessaire

function Consultation() {
  const { id } = useParams();
  const [consultation, setConsultation] = useState({});
  const [formValues, setFormValues] = useState({ ordonnance: '', bilan: '' });
  const [patientInfo, setPatientInfo] = useState({});
  const [pdfFile, setPdfFile] = useState(null);
  const [showPdf, setShowPdf] = useState(false); // État pour contrôler l'affichage du PDF
  const [idmedId, setMedecinId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`http://localhost:8000/api/get/consultations/${id}/`)
      .then(response => {
        setConsultation(response.data);
        setFormValues({ ordonnance: response.data.ordonnance, bilan: response.data.bilan });

        // Récupérer l'ID du médecin à partir de la réponse
        const medecinIdFromResponse = response.data.medecin ? response.data.medecin.idmedecin : null;
        if (medecinIdFromResponse !== null) {
          setMedecinId(medecinIdFromResponse);
        }
        
        // Récupérer les informations du patient associé à la consultation
        api.get(`http://localhost:8000/api/patients/${response.data.patient.id}/`)
          .then(res => setPatientInfo(res.data))
          .catch(error => console.error('Error fetching patient information:', error));
      })
      .catch(error => console.error('Error fetching consultation details:', error));
  }, [id]);

  const handlePdfChange = (e) => {
    const file = e.target.files[0]; // Récupérer le premier fichier sélectionné
    setPdfFile(file); // Mettre à jour l'état avec le fichier PDF
  };

  const handleViewPdf = () => {
    setShowPdf(true); // Afficher le PDF lors du clic sur le bouton "Voir PDF"
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValues(prevValues => ({ ...prevValues, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Envoi du formulaire pour mettre à jour l'ordonnance et le bilan
    api.post(`http://localhost:8000/api/update/consultations/${id}/`, formValues)
      .then(response => {
        console.log('Consultation updated successfully:', response.data);
        // Appeler handleSavePdf pour enregistrer le fichier PDF
        handleSavePdf();
        // Naviguer vers la page HomeMedecin avec l'ID du médecin
        if (idmedId !== null) {
          navigateToHomeMedecin(idmedId);
        }
      })
      .catch(error => console.error('Error updating consultation:', error));
  };

  const handleDeleteConsultation = () => {
    confirmAlert({
      title: 'Supprimer la consultation',
      message: 'Êtes-vous sûr de vouloir supprimer cette consultation ?',
      buttons: [
        {
          label: 'Oui, supprimer',
          onClick: () => {
            api.delete(`http://localhost:8000/api/delete/consultations/${id}/`)
              .then(response => {
                console.log('Consultation deleted successfully:', response.data);
                // Naviguer vers la page HomeMedecin avec l'ID du médecin
                if (idmedId !== null) {
                  navigateToHomeMedecin(idmedId);
                }
              })
              .catch(error => console.error('Error deleting consultation:', error));
          },
        },
        {
          label: 'Annuler',
        },
      ],
    });
  };
     // Dans le composant où vous liez vers la page HomeMedecin
    const navigateToHomeMedecin = (idmedId) => {
       navigate(`/login/home_medecin/${idmedId}`, { state: { idmed_id: idmedId } });
     };



  // Gérez l'enregistrement du fichier PDF
  const handleSavePdf = async () => {
    if (pdfFile) {
      try {
        const formData = new FormData();
        formData.append('pdf_file', pdfFile);
        const response = await api.post(`http://localhost:8000/api/save/pdf/${id}/`, formData);
        console.log('PDF saved successfully:', response.data);
      } catch (error) {
        console.error('Error saving PDF:', error);
      }
    } else {
      console.error('No PDF file selected.');
    }
  };

  return (
    <div>
      <h1>Consultation Details</h1>
      <p>Date: {consultation.date}</p>
      <p>Heure: {consultation.heure}</p>
      <p>Email du patient: {patientInfo.email}</p>
      <p>Nom du patient: {patientInfo.nom}</p>
      <p>Prénom du patient: {patientInfo.prenom}</p>

      <form onSubmit={handleSubmit}>
        <label>
          Ordonnance:
          <textarea name="ordonnance" value={formValues.ordonnance} onChange={handleChange} />
        </label>
        <label>
          Bilan:
          <textarea name="bilan" value={formValues.bilan} onChange={handleChange} />
        </label>
        <input type="file" accept=".pdf" onChange={handlePdfChange} />
        <button type="button" onClick={handleViewPdf}>Voir PDF</button>
        <button type="submit" className="register_patient_button" >Enregistrer</button>
        <button type="button" className="register_button" onClick={handleDeleteConsultation}>Supprimer</button>
      </form>
      
      {showPdf && pdfFile && (
        <div>
          <h2>Contenu du PDF</h2>
          {/* Afficher ici le contenu du PDF */}
          <embed src={URL.createObjectURL(pdfFile)} type="application/pdf" width="100%" height="600px" />
        </div>
      )}

      {showPdf && !pdfFile && (
        <div>
          <p>Aucun fichier PDF sélectionné.</p>
        </div>
      )}
    </div>
  );
}

export default Consultation;
