import React, { useState } from 'react';
import { render } from "react-dom";
import { createBrowserHistory } from "history";

import CreateTemplate from './containers/CreateTemplate/CreateTemplate';
import UploadTemplate from './containers/UploadTemplate/UploadTemplate';
import CreateGroups from './containers/CreateGroups/CreateGroups';
import ShowGroups from './containers/ShowGroups/ShowGroups';
import cookie from 'react-cookies';


function WizardForm(props) {
  console.log("ATTRIBUTES", attributes);
  const [attributes, setAttributes] = useState(cookie.get('attributes'));
  const [preferences, setPreferences] = useState(cookie.get('preferences'));
  const [modules, setModules] = useState(cookie.get('modules'));
  const [options, setOptions] = useState({});
  const [attributesBounds, setAttributesBounds] = useState({});
  const [preferencesNumber, setPreferencesNumber] = useState(cookie.get('preferences_number'));
  const [groupsNumber, setGroupsNumber] = useState('Groups');
  const [minStudents, setMinStudents] = useState('Min');
  const [maxStudents, setMaxStudents] = useState('Max');
  const [students, setStudents] = useState([]);
  const [capacity, setCapacity] = useState({});
  const [step, setStep] = useState(1);
  const [bounds, setBounds] = useState({});
  const [groups, setGroups] = useState([]);
  const [factible, setFactible] = useState(false);
  const [tmax, setTmax] = useState(90);
  const [sameDay, setSameDay] = useState(false);

  function wizard() {
    switch (step) {
      case 1: return <CreateTemplate step={step} setStep={setStep} 
                                     attributes={attributes} setAttributes={setAttributes}
                                     preferences={preferences} setPreferences={setPreferences}
                                     modules={modules} setModules={setModules}
                                     preferencesNumber={preferencesNumber} 
                                     setPreferencesNumber={setPreferencesNumber}/>
      case 2: return <UploadTemplate step={step} setStep={setStep} 
                                     attributes={attributes}
                                     preferences={preferences} 
                                     modules={modules}
                                     preferencesNumber={preferencesNumber} 
                                     options={options}
                                     setOptions={setOptions}
                                     setStudents={setStudents} />
      case 3: 
        return <CreateGroups step={step} setStep={setStep}
                              attributes={attributes} 
                              preferences={preferences} 
                              modules={modules}
                              options={options} 
                              students={students}
                              attributesBounds={options} 
                              setAttributesBounds={setAttributesBounds}
                              capacity={capacity} setCapacity={setCapacity}
                              minStudents={minStudents} setMinStudents={setMinStudents}
                              maxStudents={maxStudents} setMaxStudents={setMaxStudents}
                              groupsNumber={groupsNumber} setGroupsNumber={setGroupsNumber}
                              bounds={bounds} setBounds={setBounds}
                              preferencesNumber={preferencesNumber}
                              setGroups={setGroups}
                              setFactible={setFactible}
                              tmax={tmax} setTmax={setTmax}
                              sameDay={sameDay} setSameDay={setSameDay} />
      case 4: return <ShowGroups step={step} setStep={setStep} 
                                 groups={groups} students={students}
                                 attributes={attributes}
                                 preferences={preferences} 
                                 modules={modules}
                                 preferencesNumber={preferencesNumber}
                                 factible={factible}/>
      default: return <CreateTemplate step={step} setStep={setStep}/>
    }
  }
  return (
    <div>
      {wizard()}
    </div>
  );
}

function App() {
  return <WizardForm/>;
};

export default App;

const container = document.getElementById("app");
render(
  <App/>,
  container
);