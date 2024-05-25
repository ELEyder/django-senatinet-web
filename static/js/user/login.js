// Design
const wrapper = document.querySelector('.wrapper');
        const signUpLink = document.querySelector('.signUp-link');
        const signInLink = document.querySelector('.signIn-link');
        const toggleLogin = document.querySelector('.toggle-login');
        const close = document.querySelector('.close');

        signUpLink.addEventListener('click', () => {
            wrapper.classList.toggle('show-sign');
            wrapper.classList.add('show-bg');
            wrapper.style.height = '620px'; 
        })

        signInLink.addEventListener('click', () => {
            wrapper.classList.toggle('show-sign');
            wrapper.classList.add('show-bg');
            wrapper.style.height = '500px';
        })

        toggleLogin.addEventListener('click', () => {
            toggleLogin.classList.toggle('active');
            wrapper.classList.toggle('active');
        })

        close.addEventListener('click', () => {
            toggleLogin.classList.toggle('active');
            wrapper.classList.toggle('active');
            wrapper.classList.remove('show-bg');
        })