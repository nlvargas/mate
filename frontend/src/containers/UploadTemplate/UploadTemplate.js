import React, { useState } from 'react';
import axios from 'axios';
import regeneratorRuntime from "regenerator-runtime";

const style = {cont: {backgroundColor: "lightgray", padding: 25, flex: 1, backgroundSize: 'cover', align: 'center'}}


export default function CreateGroupsForm(props) {
  const { step, setStep, setOptions, options, setStudents, 
          attributes, modules, preferencesNumber } = props;
  const [selectedFile, setSelectedFile] = useState(null);
  const [nextDisabled, setNextDisabled] = useState(true);

  function onFileChange(event) {
    setSelectedFile(event.target.files[0]); 
  }

  async function onFileUpload() { 
    const formData = new FormData();
    formData.append("attributes", attributes); 
    formData.append("modules", modules);
    formData.append("preferencesNumber", preferencesNumber);
    formData.append("file", selectedFile, selectedFile.name); 
    try {
      let response = await axios.post("api/upload/", formData)
      alert("Su plantilla ha sido cargada correctamente");
      console.log(response)
      setOptions(JSON.parse(response.data.a));
      setStudents(JSON.parse(response.data.students))
      setNextDisabled(false);
    } catch(err) {
      console.log("Error fetching data-----------", err);
    }
  }; 
   

  return (
      <div>
      <div style={style.cont}>
      <h3> Subir template </h3>
      <input type="file" onChange={onFileChange}/>
      <button onClick={() => onFileUpload()}>Subir</button>
      </div>
      <p></p>
      <button onClick={() => setStep(step - 1)}> Atras </button>
      <button disabled={nextDisabled} onClick={() => setStep(step + 1)}> Siguiente </button>
      </div>
    );
};
