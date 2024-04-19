import React from "react";
import FormPatient from "../components/FormPatient";
import { useParams } from 'react-router-dom';
function RegisterPatient() {
  const { medecinId } = useParams();
  return <FormPatient medecinId={medecinId} route="api/user/patientReg/" />;
}

export default RegisterPatient;
