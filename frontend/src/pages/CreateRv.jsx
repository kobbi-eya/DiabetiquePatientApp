import React from "react";
import FormRv from "../components/FormRendezVous";
import { useParams } from 'react-router-dom';

function CreateRv() {
  const { medecinId } = useParams();
  return <FormRv medecinId={medecinId} route="api/user/createRv/" />;
  //return <fetchPatientIdByEmail route="api/user/getPatientByEmail/<str:email>/</str:email>" />;
}
export default CreateRv;

