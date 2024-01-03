import React, { useState } from 'react';
import styled from 'styled-components';
import CommentListItem from './CommentListItem';


const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;

    :not(:last-child) {
        margin-bottom: 16px;
    }
`;

function CommentList(props) {
    const { comments } = props;

    // Ensure comments is always an array
    const safeComments = comments || [];

    const [newComment, setNewComment] = useState('');

    const handleSubmit = async () => {
        // Your code to submit the newComment to the server
        // You can use fetch or axios to send the comment data
        // Example:
        // const response = await fetch('http://your-api-url', {
        //     method: 'POST',
        //     body: JSON.stringify({ comment: newComment }),
        //     headers: {
        //         'Content-Type': 'application/json',
        //         // Add any necessary headers, like authorization
        //     },
        // });

        // Clear the input field after submission
        setNewComment('');
    };

    return (
        <Wrapper>
            {safeComments.map((comment, index) => {
                return (
                    <div key={comment.id}>
                        <p>{comment.user}: {comment.comment}</p>
                    </div>
                );
            })}
        </Wrapper>
    );
}

export default CommentList;