import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { Box } from '@mui/material';



const getCookieValue = (name) => (
  document.cookie.split('; ').find(row => row.startsWith(name + '='))
  ?.split('=')[1]
);

const yourAuthToken = localStorage.getItem('token');

const ImgMediaCard = ({ id, title, text, imagePath, likeStatus, url }) => {
  console.log('likeStatus:', likeStatus);
  console.log('userId:', id);
  const userId = getCookieValue('nickname'); // 쿠키에서 userId 가져오기
  const [liked, setLiked] = useState(likeStatus && likeStatus.includes(userId)); // userId는 현재 로그인한 사용자의 ID

  // 텍스트를 요약해서 표시할 길이를 설정합니다.
  const summaryLength = 200; // 예시로 200글자로 설정합니다.
  const [isTextTooLong, setIsTextTooLong] = useState(text.length > summaryLength);

  const handleLike = async () => {
    console.log("Current userId:", userId); // 현재 로그인한 사용자 ID 출력
    try {
      const response = await fetch(`http://127.0.0.1:8000/crawling/like/`, {
        method: 'POST',
        headers: {
          'Authorization' : `Bearer ${yourAuthToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user: Number(userId), // 현재 로그인한 사용자 이름, 매번 캐시비우기 및 강력새로고침을 해야하나..
          crawling: id  // 좋아요를 누른 게시물의 id
        })
      });
  
      if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(`Error: ${response.status}, Message: ${errorMessage}`);
      }
      const data = await response.json(); // 서버 응답 처리
      setLiked(data.liked); // 예시: 서버에서 'liked' 상태를 응답으로 보내줄 경우
    } catch (error) {
      console.error('Failed to like/unlike:', error);
    }
  };
  

  // 'MORE' 버튼 클릭 핸들러
  const handleReadMore = () => {
    window.location.href = url; // URL로 리디렉션
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', m: 2 }}>
      <Card sx={{ maxWidth: 345, boxShadow: 3, display: 'flex', flexDirection: 'column', height: '100%' }}>
        {imagePath && (
          <CardMedia
            component="img"
            alt={title}
            height="140"
            image={imagePath}
            sx={{ objectFit: 'cover' }}
          />
        )}
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography gutterBottom variant="h5" component="div">
            {title}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {isTextTooLong ? `${text.substring(0, summaryLength)}...` : text}
          </Typography>
        </CardContent>
        <CardActions sx={{ justifyContent: 'center' }}>
          <Button size="small" onClick={handleLike} sx={{ color: liked ? 'error.main' : 'primary.main' }}>
            <FavoriteIcon />
            LIKE
          </Button>
            <Button size="small" onClick={handleReadMore}>
              MORE
            </Button>
        </CardActions>
      </Card>
    </Box>
  );
};

export default ImgMediaCard;