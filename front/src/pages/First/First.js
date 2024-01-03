import React, { useState, useEffect } from 'react';
import ImgMediaCard from './Firstcard';
import { useAuth } from '../../context/AuthContext'; // AuthContext의 위치에 따라 경로를 적절히 수정해주세요.

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
            {isLoggedIn ? ( // 로그인 상태에 따라 다른 컨텐츠를 보여줍니다.
                <>
                    <h2>Recommended for You</h2>
                    {recommendations.length > 0 ? (
                        recommendations.map((recommendation, index) => (
                            <ImgMediaCard
                                key={index}
                                id={recommendation.id}
                                title={`제목: ${recommendation.title}`}
                                text={`설명: ${recommendation.body}`} // body로 변경
                                imagePath={recommendation.image}
                                likeStatus={recommendation.like_status} // '좋아요' 상태 추가
                            />
                        ))
                    ) : (
                        <p>No recommendations available</p>
                    )}
                </>
            ) : (
                <p>로그인이 필요합니다.</p>
            )}
        </div>
    );
};

export default Mylist;