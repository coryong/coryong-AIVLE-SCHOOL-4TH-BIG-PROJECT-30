import React, { useState, useEffect } from 'react';
import ImgMediaCard from './Mediacard';
import { useNavigate } from 'react-router-dom'; // 추가
 
const Mylist = () => {
    const [recommendations, setRecommendations] = useState([]);
    const navigate = useNavigate(); // 추가

    const getCookieValue = (name) => (
        document.cookie.split('; ').find(row => row.startsWith(name + '='))
        ?.split('=')[1]
    );
    const handleMoreClick = (postId) => {// 추가
        navigate(`/recommend/Recommend/${postId}`);// 추가
    };// 추가
    const fetchRecommendations = async () => {
        const nickname = getCookieValue('nickname');
        if (!nickname || nickname === 'undefined') {
            console.error('Nickname is not found or undefined');
            return;
        }
        const apiUrl = `http://127.0.0.1:8000/constest/?nickname=${nickname}`;
        console.log('Sending nickname to server:', nickname, apiUrl);
        try {
            const response = await fetch(apiUrl, { method: 'GET', credentials: 'include' });
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            const data = await response.json();
            console.log(data);
            setRecommendations(data.recommend_post_ids);
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
        }
    };
    useEffect(() => {//버튼을 누르지않아도 바로 추천시스템이 보이는 기능
        fetchRecommendations();
    }, []);

    const CardContainer = ({ children }) => {
        return (
          <div style={{
            display: 'flex',
            flexWrap: 'wrap', // Ensures that the cards will wrap to the next line if there's not enough space
            justifyContent: 'center', // Centers the cards within the container
            gap: '16px' // Adds a 2px gap between cards
          }}>
            {children}
          </div>
        );
      };
 
    return (
<div>
<h2>Recommended for You</h2>
        {recommendations.length > 0 ? (
<CardContainer> {/* Use CardContainer here */}
                {recommendations.map((recommendation, index) => (
<ImgMediaCard
                        key={index}
                        title={`제목: ${recommendation.title}`}
                        text={`설명: ${recommendation.Exp_require}`}
                        buttonText="More"
                        imagePath={`http://127.0.0.1:8000${recommendation.image}`}
                        onMoreClick={() => handleMoreClick(recommendation.id)} // 추가
                    />
                ))}
</CardContainer>
        ) : (
<p>No recommendations available</p>
        )}
</div>
  );
};
 
export default Mylist;