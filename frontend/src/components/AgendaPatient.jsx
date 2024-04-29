import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; // Importer useParams
import api from '../api'; 

function Agenda() {
    const [rendezVous, setRendezVous] = useState([]);
    const { patientId } = useParams(); // Récupérer l'ID du patient depuis les paramètres d'URL

    useEffect(() => {
        const fetchRendezVous = async () => {
            try {
                const response = await api.get(`api/rendez-vous-patient/${patientId}/`); // Utiliser l'ID du patient dans la requête API
                setRendezVous(response.data.rendez_vous);
            } catch (error) {
                console.error('Erreur lors de la récupération des rendez-vous:', error);
            }
        };

        fetchRendezVous();
    }, [patientId]); // Ajouter patientId comme dépendance pour rafraîchir les rendez-vous lorsque l'ID du patient change

    return (
        <div>
            <h2>Agenda des Rendez-vous</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date rendez-vous</th>
                        <th>Heure rendez-vous</th>
                        <th>Nom & prenom du Médecin</th>
                        <th>Mobile Medecin</th>
                    </tr>
                </thead>
                <tbody>
                    {rendezVous.map(rendezVous => (
                        <tr key={rendezVous.id}>
                            <td>{rendezVous.date_consultation}</td>
                            <td>{rendezVous.heure_consultation}</td>
                            <td>{rendezVous.nomMedecin}, {rendezVous.prenomMedecin}</td>
                            <td>{rendezVous.mobile}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <Link to={`/home_patient/${patientId}`} className="btn btn-primary">Retourner à l'accueil</Link>
        </div>
    );
}

export default Agenda;
