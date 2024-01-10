const likeBtn = document.querySelector('.heart-icon');
const numberOfLikesElement = document.querySelector('.number-of-likes');
let isLiked = false;
// Functions
const likeClick = () => {
// if the like button hasn't been clicked
  if (!isLiked) {
    likeBtn.classList.add('isLiked');
    isLiked = !isLiked;
  }
// if the like button has been clicked
 else {
    likeBtn.classList.remove('isLiked');
    isLiked = !isLiked;
  }
};
// Event Listeners
likeBtn.addEventListener('click', likeClick);