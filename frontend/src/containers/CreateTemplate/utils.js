import React, { useState, Button } from 'react';
import axios from 'axios';

const a = {"Genero": {"M": 10, "F": 10}, 
                    "Area": {"Finanzas": 0, "Gestion": 4, "Estudiante": 8}, 
                    "Comuna": {"RM": 40, "No RM": 30}, 
                    "Carrera": {"Ingenieria": 2, "Medicina": 8, "Periodismo": 10, "Teatro": 11}, 
                    "Universidad": {"PUC": 10, "UCH": 8, "UFST": 2, "UdC": 0}, 
                    "Personalidad": {"Introvertido": 9, "Extrovertido": 10}};

const p = ["Dieta Vegana", "Miigacion Huella de carbono", "Reciclaje", "Bioplasticos", "Electromovilidad"];

const m = ["Martes", "Jueves"];

export default function CreateGroupsForm() {
  const [groupsNumber, setGroupsNumber] = useState('Groups');
  const [minStudents, setMinStudents] = useState('Min');
  const [maxStudents, setMaxStudents] = useState('Max');
  const url = 'http://127.0.0.1:8000';
  const [attributes, setAttributes] = useState(a);
  const [preferences, setPreferences] = useState(p);
  const [showCreateGroups, setShowCreateGroups] = useState(false);

  async function runModelRequest() {
    const body = { attributes, 
                   preferences, 
                   groupsNumber, 
                   minStudents, 
                   maxStudents }
    const result = await axios.post(url + '/api/run_model/', body)
    //alert(result.data)
  }

  function send() {
      runModelRequest();
      console.log("Enviado");
  }

  function createAttributes() {
      let table = []
      for (const [key, value] of Object.entries(attributes)) {
          table.push(<tr><Attribute name={key} options={value} attributes={attributes} setAttributes={setAttributes}/></tr>)
      }
      return table
  };

  function editPreference(e, pref, type) {
    let prefs = preferences;
    prefs[pref][type] = parseInt(e.target.value);
    setPreferences(prefs);
  }

  return (
      <div>
      <h3> Ajustes generales </h3>
        <p>Cantidad de grupos:</p>    
        <input type="text" name="groupsNumber" onChange={(e) => setGroupsNumber(parseInt(e.target.value))}/>
        <p>Minimo de estudiantes por grupo:</p>
        <input type="text" name="minStudents" onChange={(e) => setMinStudents(parseInt(e.target.value))}/>
        <p>Maximo de estudiantes por grupo:</p>
        <input type="text" name="maxStudents" onChange={(e) => setMaxStudents(parseInt(e.target.value))}/>
       <h3> Atributos </h3>
        <table>
        {createAttributes()}
        </table>
        <h3> Preferencias </h3>
        {Object.keys(preferences).map((pref) => {
            return <p> {pref} <input type="text" name={pref} onChange={(e) => editPreference(e, pref, "min")}/> <input type="text" name={pref} onChange={(e) => editPreference(e, pref, "max")}/> </p>
        })}
      </div>
    );
};


function Attribute(props) {
  const { name, options, attributes, setAttributes } = props;

  function editOption(value, key, type) {
    let attr = attributes;
    attr[name][key][type] = parseInt(value.target.value);
    setAttributes(attr);
  }

  function createOptions() {
    let optionsToShow = []
    for (const [key, value] of Object.entries(options)) {
        optionsToShow.push(<tr> {key} </tr>)
        optionsToShow.push(<tr> Min: <input type="text" name="min" onChange={(value) => editOption(value, key, "min")}/> </tr>)
        optionsToShow.push(<tr> Max: <input type="text" name="max" onChange={(value) => editOption(value, key, "max")}/> </tr>)
    }
    return optionsToShow
  };

  return (
      <div>
        <h5>{name}</h5>
        <table>
        {createOptions()}
        </table>
      </div>
    );
}
