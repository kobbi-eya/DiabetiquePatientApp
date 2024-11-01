import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/login"
import Register from "./pages/Register"
import HomeMedecin from "./pages/HomeMedecin"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import RegisterPatient from "./pages/RegisterPatient"
import CreateRv from "./pages/CreateRv"
import CarnetMedical  from "./components/carnetmedicale"
import axios from 'axios';
import Listepatient from "./pages/listepatients" 
import Consultation from  "./components/Consultation"
import HomePatient from "./pages/HomePatient"
import CarnetMedicalPat from "./components/CarnetMedicalpat"
import ChangeDoctorForm from "./components/FormChangementDoctor"
import DoctorChangeRequests from "./components/Requests"
import Agenda from "./components/AgendaPatient"



//function RegisterAndLogout() {
  //localStorage.clear()
  //return <Register />
//}


function App() {
  return (
    <BrowserRouter>
      <Routes>
      <Route
        path="/"
        element={
    <ProtectedRoute>
      <HomeMedecin />
    </ProtectedRoute>
      }
      />
    <Route
      path="/"
      element={
    <ProtectedRoute>
      <HomePatient />
    </ProtectedRoute>
      }
    />
       
        <Route path="/login" element={<Login />} />
        <Route path="/home_patient/:patientId" element={<HomePatient />} />
        <Route path="/login/registerpatient/:medecinId" element={<RegisterPatient />} />
        <Route path="/login/CreateRv/:medecinId" element={<CreateRv />} />
        <Route path="/login/home_medecin/:medecinId" element={<HomeMedecin />} />
        <Route path="/login/ListePatient/:medecinId" element={<Listepatient />} />
        <Route path="/ListePatient/Info/:patientId" element={<CarnetMedical />} />
        <Route path="/register" element={<Register />} />
        <Route path="/consultation/:id" element={<Consultation/>} />
        <Route path="/carnet_medical/:patientId" element={<CarnetMedicalPat />} />
        <Route path="/DemandeChangementDoctor/:patientId" element={<ChangeDoctorForm />} />
        <Route path="Requests/:medId" element={<DoctorChangeRequests />} />
        <Route path="/Agenda/:patientId" element={<Agenda />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App