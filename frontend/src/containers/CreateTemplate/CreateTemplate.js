import React, { useState, Button } from 'react';
import XLSX from 'xlsx';
import { saveAs } from 'file-saver';

function s2ab(s) { 
  var buf = new ArrayBuffer(s.length); 
  var view = new Uint8Array(buf); 
  for (var i=0; i<s.length; i++) view[i] = s.charCodeAt(i) & 0xFF; 
  return buf;    
}

const style = {cont: {backgroundColor: "lightgray", padding: 25, flex: 1, backgroundSize: 'cover', align: 'center'}}

export default function CreateTemplate(props) {
  const { step, setStep, attributes, setAttributes,
          preferences, setPreferences, modules, setModules,
          preferencesNumber, setPreferencesNumber } = props;
  const [newAttribute, setNewAttribute] = useState("");
  const [newPreference, setNewPreference] = useState("");
  const [newModule, setNewModule] = useState("");
  const [showLink, setShowLink] = useState(false);
  const [wbout, setWbout] = useState("");
  const [preferencesNumberOptions, setPreferencesNumberOptions] = useState([...Array(preferencesNumber + 1).keys()])

  function addAttribute() {
    setAttributes(attributes.concat(newAttribute));
    setNewAttribute("");
  }

  function addPreference() {
    setPreferences(preferences.concat(newPreference));
    setNewPreference("");
    setPreferencesNumberOptions(preferencesNumberOptions.concat(preferencesNumberOptions.length));
  }

  function addModule() {
    setModules(modules.concat(newModule));
    setNewModule("");
  }

  function generateTemplate() {
    let wb = XLSX.utils.book_new();
    wb.SheetNames.push("Alumnos");
    let r = ["Nombre"]
    let prefNumber = 1
    attributes.forEach(attr => {
      r.push(attr);
    })
    modules.forEach(mod => {
      r.push("Disponibilidad " + mod)
    })
    const prefsNum = [...Array(preferencesNumber).keys()].map(i => i + 1)
    prefsNum.forEach(pref => {
      r.push("Preferencia " + prefNumber.toString())
      prefNumber++;
    })
    let ws_data = []
    ws_data.push(r)
    let ws = XLSX.utils.aoa_to_sheet(ws_data);
    wb.Sheets["Alumnos"] = ws;
    setWbout(XLSX.write(wb, {bookType:'xlsx', type: 'binary'}));
    setShowLink(true)
  }

  function downloadTemplate() {
    saveAs(new Blob([s2ab(wbout)], {type:"application/octet-stream"}), 'template.xlsx');
  }

  function next() {
    setStep(step + 1)
  }

  return (
      <div style={{justifyContent:'center', alignItems:'center'}}>
      <div style={style.cont}>
        <h3> Atributos </h3>
        {attributes.map((item, index) => (<p> {item} </p>))}
        <input type="text" value={newAttribute} onChange={(e) => setNewAttribute(e.target.value)}/>
        <button onClick={addAttribute}> Agregar atributo </button>
      </div>
      <p></p> 
      <div style={style.cont}>
        <h3> Preferencias </h3>
        {preferences.map((item, index) => (<p> {item} </p>))}
        <input type="text" value={newPreference} onChange={(e) => setNewPreference(e.target.value)}/>
        <button onClick={addPreference}> Agregar preferencia </button>
        <p></p>
        <label>Numero de preferencias a elegir</label>
        <select value={preferencesNumber} onChange={(e) => setPreferencesNumber(e.target.value)}>
        {preferencesNumberOptions.map((x,y) => (<option key={y}>{x}</option>))}
        </select>
      </div>
      <p></p>
      <div style={style.cont}>
        <h3> Modulos </h3>
        {modules.map((item, index) => (<p> {item} </p>))}
        <input type="text" value={newModule} onChange={(e) => setNewModule(e.target.value)}/>
        <button onClick={addModule}> Agregar modulo </button>  
      </div>
        <p></p>
        <div style={style.cont}>
        <button onClick={generateTemplate}> Crear Template </button>
        {showLink && <button onClick={downloadTemplate}> Descargar template </button>}
        </div>
        <p></p>
        <button onClick={next} class="btn-get-started scrollto"> Siguiente </button>
      </div>
    );
};
