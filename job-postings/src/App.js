import React, { useState, useEffect } from 'react';
import './App.css'; // Style the main app container similarly
import JobListing from './components/JobListings'; // Add 's' to match the filename

const App = () => {
  const [jobPostings, setJobPostings] = useState([]);

  useEffect(() => {
    fetch('/data/df.json')
      .then(response => response.json())
      .then(data => setJobPostings(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="app-container">
      <header>Jobtify</header>
      {jobPostings.map((job, index) => (
        <JobListing key={index} job={job} />
      ))}
    </div>
  );
};

export default App;
