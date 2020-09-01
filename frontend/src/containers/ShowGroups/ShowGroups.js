import React, { useState, useEffect, Button } from 'react';
import XLSX from 'xlsx';
import { saveAs } from 'file-saver';

const style = {cont: {backgroundColor: "lightgray", padding: 25, flex: 1, backgroundSize: 'cover', align: 'center'}}

function s2ab(s) { 
  var buf = new ArrayBuffer(s.length); 
  var view = new Uint8Array(buf); 
  for (var i=0; i<s.length; i++) view[i] = s.charCodeAt(i) & 0xFF; 
  return buf;    
}


function Students(props) {
  const { groupStudents, students, name } = props;
  const [show, setShow] = useState(false);
  console.log("Students")
  console.log(students)

  function createStudents() {
    let table = []
    groupStudents.forEach(item => {
        table.push(<tr>{item}</tr>)
    })
    return table
  }

  return (
    <div>
      <h5 onClick={() => setShow(!show)}> {name} </h5>
      {show &&
        <div>
        <table>
          {createStudents()}
        </table>
        <p></p>
        <p></p>
        </div>
      }
    </div>
  )
}



export default function ShowGroups(props) {
  const { step, setStep, groups, students, 
          attributes, preferencesNumber, 
          modules, factible } = props;
  let studentsDict = students.reduce(function(obj, x) {
      obj[x.id] = x;
      return obj;
  }, {});

  const [wbout, setWbout] = useState("");
  
  useEffect(() => {
    if (!factible) {
      alert("Los grupos presentados a continuacion no cumplen con todas las restricciones anteriores. Revise esta solución, presione 'Atras', edite las restricciones y vuelva a correr el modelo.")
    }
    generateTemplate();
  }, []);

  function createGroups() {
    let table = []
    groups.forEach(item => {
        table.push(<tr><Students name={item.group} groupStudents={item.students} students={students}/></tr>)
    })
    return table
  };

  function generateTemplate() {
    let wb = XLSX.utils.book_new();
    wb.SheetNames.push("Grupos");
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
    groups.forEach(item => {
      ws_data.push([item.group])
      ws_data.push(r)
      let students = item.students;
      students.forEach(student => {
        let studentInfo = [student];
        studentInfo = studentInfo.concat(studentsDict[student].attributes)
        studentInfo = studentInfo.concat(studentsDict[student].disponibilities)
        studentInfo = studentInfo.concat(studentsDict[student].preferences)
        ws_data.push(studentInfo)
      })
      ws_data.push([])
    })
    let ws = XLSX.utils.aoa_to_sheet(ws_data);
    wb.Sheets["Grupos"] = ws;
    setWbout(XLSX.write(wb, {bookType:'xlsx', type: 'binary'}));
  }

  function downloadTemplate() {
    saveAs(new Blob([s2ab(wbout)], {type:"application/octet-stream"}), 'grupos.xlsx');
  }


  return (
    <div>
      <div style={style.cont}>
      <h3> Grupos </h3>
      <table>
      {createGroups()}
      </table>
      </div>
      <p></p>
      <button onClick={() => setStep(step - 1)}> Atras </button>
      <button onClick={downloadTemplate} > Descargar Excel </button>
    </div>
    );
};