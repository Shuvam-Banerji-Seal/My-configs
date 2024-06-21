document.querySelector('.main-profile').addEventListener('mouseenter', () => {
    document.querySelectorAll('.student-profile').forEach(profile => {
        profile.style.opacity = '1';
        profile.style.transform = 'translate(0, 0)';
    });

    document.querySelectorAll('.line').forEach(line => {
        line.style.transform = 'scaleY(1)';
    });
});

document.querySelector('.main-profile').addEventListener('mouseleave', () => {
    document.querySelectorAll('.student-profile').forEach(profile => {
        profile.style.opacity = '0';
        profile.style.transform = 'translate(50%, 50%)';
    });

    document.querySelectorAll('.line').forEach(line => {
        line.style.transform = 'scaleY(0)';
    });
});
