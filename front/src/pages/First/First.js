import React, { useState, useEffect } from 'react';
import ImgMediaCard from './Firstcard';
import { useAuth } from '../../context/AuthContext'; // AuthContext의 위치에 따라 경로를 적절히 수정해주세요.
import { Box } from '@mui/material'; // 'Box'를 여기서 임포트합니다.

const Mylist = () => {
    const { isLoggedIn} = useAuth(); // 로그인 상태와 토큰을 가져옵니다.
    const [recommendations, setRecommendations] = useState([]);
    const token = localStorage.getItem('token'); // 로컬 스토리지에서 토큰을 가져옵니다.

    const fetchRecommendations = async () => {
        if (!isLoggedIn) return; // 로그인이 되어있지 않으면 추천 목록을 가져오지 않습니다.

        const apiUrl = `http://127.0.0.1:8000/crawling/crawlingview/`;
        try {
            const response = await fetch(apiUrl, { 
                method: 'GET', 
                credentials: 'include',
                headers: { 'Authorization': `Bearer ${token}` } // 토큰을 헤더에 포함시킵니다.
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            const data = await response.json();
            setRecommendations(data);
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
        }
    };

    useEffect(() => {
        fetchRecommendations();
    }, [isLoggedIn]); // 로그인 상태가 변경될 때마다 추천 목록을 다시 가져옵니다.

    return (
        <div>
          {isLoggedIn ? (
            <>
              <h2>Recommended for You</h2>
              <Box sx={{ 
                display: 'flex', 
                flexWrap: 'wrap', // 여기에 flex-wrap을 적용합니다.
                justifyContent: 'center', // 중앙 정렬
                gap: 2 // 카드 사이의 간격을 줍니다.
              }}>
                {recommendations.length > 0 ? (
                  recommendations.map((recommendation, index) => (
                    <ImgMediaCard
                      key={index}
                      id={recommendation.id}
                      title={`${recommendation.title}`}
                      text={` ${recommendation.body}`} // body로 변경
                      imagePath={recommendation.image}
                      likeStatus={recommendation.like_status} // '좋아요' 상태 추가
                      url={recommendation.url} // 'url' prop 추가
                    />
                  ))
                ) : (
                  <p>No recommendations available</p>
                )}
              </Box>
            </>
          ) : (
            <p>로그인이 필요합니다.</p>
          )}
        </div>
      );
    };
    
    export default Mylist;