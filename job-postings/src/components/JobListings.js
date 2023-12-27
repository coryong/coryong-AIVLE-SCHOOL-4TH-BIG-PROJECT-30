import React from 'react';
import './JobListing.css';
import DefaultLogo from '../assets/wanted.jpg'; // 'wanted.jpg' 이미지를 import 합니다.

const JobListing = ({ job }) => {
  const logoSrc = job.logo ? job.logo : DefaultLogo; // logo가 없을 경우 대체 이미지를 사용합니다.

  return (
    <div className="job-listing">
      <div className="job-icon">
        <img src={logoSrc} alt={`${job.회사명} logo`} />
      </div>
      <div className="job-info">
        <h3>{job.직업}</h3>
        <p>{job.회사명}</p>
        {/* Additional information */}
        <p><strong>주요업무:</strong> {job.주요업무}</p>
        <p><strong>자격요건:</strong> {job.자격요건}</p>
        <p><strong>우대사항:</strong> {job.우대사항}</p>
        <p><strong>복지:</strong> {job.복지}</p>
        <p><strong>기술 스택:</strong> {job.기숤}</p>
      </div>
    </div>
  );
};

export default JobListing
