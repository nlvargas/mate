import React, { useState, Button, useEffect } from 'react';
import axios from 'axios';

const style = {cont: {backgroundColor: "lightgray", padding: 25, flex: 1, backgroundSize: 'cover', align: 'center'},
               cont2: {backgroundColor: "gray", padding: 5, flex: 1, backgroundSize: 'cover', align: 'center'}}

function Loader() {
  return (
    <div className="loader center">
      <i className="fa fa-cog fa-spin" />
    </div>
  );
}


export default function CreateGroups(props) {
  const { step, setStep, groupsNumber, setGroupsNumber,
          minStudents, setMinStudents, maxStudents, setMaxStudents,
          attributes, setAttributes, preferences, setPreferences,
          modules, setModules, preferencesNumber, tmax, setTmax,
          options, students, capacity, setCapacity, setGroups, setFactible,
          sameDay, setSameDay } = props;

  const [buttonText, setButtonText] = useState("Generar grupos")
  const [loading, setLoading] = useState(true);
  const [bounds, setBounds] = useState({});
  const [prefsBounds, setPrefsBounds] = useState({});
  let fDay = {}
  modules.forEach(module => {
    fDay[module] = {};
    preferences.forEach(pref => {
      fDay[module][pref] = false;
    })
  })
  const [fixedDay, setFixedDay] = useState(fDay);
  

  function validate() {
    if (students.length/groupsNumber <= maxStudents && students.length/groupsNumber >= minStudents) {
      return true
    } else {
      alert("Alguno de los parametros ingresados en Ajustes Generales provoca infactibilidad en el modelo. Por favor revisar y volver a intentar.")
      return false
    }
  }
  
  async function runModelRequest() {
    if (validate()) {
      const body = JSON.stringify({ attributes, 
        preferences, 
        groupsNumber, 
        minStudents, 
        maxStudents,
        bounds,
        students,
        capacity,
        preferencesNumber,
        options,
        prefsBounds,
        modules,
        tmax,
        sameDay,
        fixedDay })
        setButtonText("Creando grupos...")
        const result = await axios.post('/api/run_model/', body);
        const json_result = JSON.parse(result.data)
        setGroups(json_result.results);
        setFactible(json_result.factible)
        setButtonText("Generar grupos")
        setStep(step + 1)
    }
  }

  useEffect(() => {
    let cap = {}
    let fDay = {}
    modules.forEach(module => {
      cap[module] = students.length;
      fDay[module] = {};
      preferences.forEach(pref => {
        fDay[module][pref] = false;
      })
    })
    setFixedDay(fDay);
    setCapacity(cap);
  }, []);

  function createAttributes() {
      let table = []
      for (const [key, value] of Object.entries(options)) {
          table.push(<tr><Attribute name={key} 
                                    options={value} 
                                    attributes={options} 
                                    setBounds={setBounds}
                                    bounds={bounds}
                                    groupsNumber={groupsNumber}
                                    maxStudents={maxStudents}/></tr>)
      }
      return table
  };

  function editModule(e, mod) {
    let cap = capacity;
    cap[mod]= parseInt(e.target.value);
    setCapacity(cap);
  }

  function createSettings() {
    let optionsToShow = []
        optionsToShow.push(<tr>
          Cantidad de grupos ({students.length} alumnos):
          <input style={{float:"right", width: "60px"}} size="4" type="number" name="groupsNumber" onChange={(e) => setGroupsNumber(parseInt(e.target.value))}/>
          </tr>)
        optionsToShow.push(<tr>
          Minimo de estudiantes por grupo:
          <input style={{float:"right", width: "60px"}} size="4" type="number" name="minStudents" onChange={(e) => setMinStudents(parseInt(e.target.value))}/>
          </tr>)
        optionsToShow.push(<tr>
          Maximo de estudiantes por grupo:
          <input style={{float:"right", width: "60px"}}  size="4" type="number" name="maxStudents" onChange={(e) => setMaxStudents(parseInt(e.target.value))}/>
          </tr>)
        optionsToShow.push(<tr>
          Tiempo máximo para asignar los grupos (en minutos):
          <input style={{float:"right", width: "60px"}}  size="4" type="number" name="maxStudents" defaultValue={tmax} onChange={(e) => setTmax(parseInt(e.target.value))}/>
          </tr>)
    return optionsToShow
  };

  function createPreferences() {
    let table = []
    preferences.forEach(pref => {
        table.push(<tr><Preference pref={pref} 
                                   setPrefsBounds={setPrefsBounds}
                                   prefsBounds={prefsBounds} 
                                   groupsNumber={groupsNumber}/></tr>)
    })
    return table
  };

  function editFixedDay(mod, pref, value) {
    let f = fixedDay[mod];
    f[pref] = value;
    setFixedDay({...fixedDay, mod: f});
  }

  return (
      <div>
      <div style={style.cont}>
      <h3> Ajustes generales </h3>
      <table>
        {createSettings()}
      </table>
      </div>
      <p></p>
      <div style={style.cont}>
       <h3> Atributos </h3>
        <table>
        {createAttributes()}
        </table>
      </div>
    <p></p>
      <div style={style.cont}>
        <h3> Preferencias </h3>
        <table>
        {createPreferences()}
        </table>
      </div>
      <p></p>
      <div style={style.cont}>
        <h3> Modulos </h3>
        {modules.map((mod, index) => {
            return (
              <p>  
              <div key={students.length}>
              <label> Capacidad {mod}: </label>
              <input style={{float:"right", width: "60px"}} defaultValue={students.length || ""} size="4" type="number" name={mod} onChange={(e) => editModule(e, mod)}/> 
              {preferences.map((pref, index) => {
                return <tr> Preferencia {pref} solo en este modulo: <button onClick={() => editFixedDay(mod, pref, !fixedDay[mod][pref])}> {fixedDay[mod][pref] ? "Desactivar" : "Activar"} </button></tr>
              })}
              </div>
              </p>
            )
        })}
        <tr> Grupos con la misma preferencia deben ser asignados el mismo dia: <button onClick={() => setSameDay(!sameDay)}> {sameDay ? "Desactivar" : "Activar"} </button></tr>
      </div>
      <p></p>
        <button onClick={() => setStep(step - 1)}>
          Atras
        </button>
        <button onClick={runModelRequest}>
          {buttonText}
        </button>
      </div>
    );
};

function Preference(props) {
  const { pref, prefsBounds, setPrefsBounds, groupsNumber} = props;
  const [show, setShow] = useState(false);

  function editPreference(e, pref, type) {
    let prefs = prefsBounds;
    if (!(pref in prefs)) {
      prefs[pref] = {"min": 0, "max": groupsNumber}
    }
    prefs[pref][type] = parseInt(e.target.value);
    setPrefsBounds(prefs);
  }
  return (
    <div> 
    <h4 onClick={() => setShow(!show)}>- {pref} </h4>
    {show && 
      <div key={groupsNumber}>
        <table>
        <tr>
        Mín. cantidad de grupos con esta preferencia: 
        <input defaultValue={0} style={{float:"right", width: "60px"}}  maxlength="4" type="number" name={pref} onChange={(e) => editPreference(e, pref, "min")}/> 
        </tr>
        <tr>
        Máx. cantidad de grupos con esta preferencia: 
        <input defaultValue={groupsNumber || ""} style={{float:"right", width: "60px"}}  maxlength="4" type="number" name={pref} onChange={(e) => editPreference(e, pref, "max")}/> </tr>
        </table>
      </div>}
    </div>
  )
}

function Attribute(props) {
  const { name, options, attributes, setBounds, bounds, maxStudents } = props;
  const [check, setCheck] = useState({})
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    let c = check;
    for (const [key, value] of Object.entries(options)) {
      c[key] = "Activar";
    }
    setCheck(c);
  }, []);

  function editOption(value, key, type) {
    let b = bounds;
    if (!(key in b)) {
      b[key] = {"min": 0, "max": maxStudents, "solo": false}
    }
    b[key][type] = parseInt(value.target.value);
    setBounds(b);
  }

  function changeRadio(key) {
    let b = bounds;
    let c = check;
    if (!(key in b)) {
      b[key] = {"min": 0, "max": maxStudents, "solo": false}
    }
    b[key]["solo"] = !b[key]["solo"]
    console.log(b[key])
    if (!b[key]["solo"]) {
      c[key] = "Activar";
    } else {
      c[key] = "Desactivar";
    }
    setCheck({...check, key: "Desactivar"});
    setBounds(b);
  }

  function createOptions() {
    let optionsToShow = []
    for (const [key, value] of Object.entries(options)) {
        optionsToShow.push(<tr> <h5>{key}</h5>({attributes[name][key]} alumnos marcaron esta opcion)</tr>)
        optionsToShow.push(<tr> Min: <input defaultValue={0} style={{width: "60px"}} type="number" name="min" onChange={(value) => editOption(value, key, "min")}/> Max: <input defaultValue={maxStudents || ""} style={{width: "60px"}} type="number" name="max" onChange={(value) => editOption(value, key, "max")}/> </tr>)
        optionsToShow.push(<tr> No pueden haber alumnos solos: 
        <button onClick={() => changeRadio(key)}> {check[key]} </button></tr>)
        optionsToShow.push(<tr> <p></p></tr>)
    }
    return optionsToShow
  };

  return (
      <div>
        <h4 onClick={() => setShowSettings(!showSettings)}>- {name}</h4>
        { showSettings &&
          <div key={maxStudents}>
          <table>
          {createOptions()}
          </table>
          </div>
        }
      </div>
    );
}

