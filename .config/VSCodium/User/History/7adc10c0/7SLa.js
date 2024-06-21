document.addEventListener('DOMContentLoaded', () => {
    const mainProfile = document.getElementById('mainProfile');
    const studentProfiles = document.querySelectorAll('.student-profile');
    const lines = document.querySelectorAll('.line');
    const container = document.querySelector('.container');

    let linesCoords = [
        { x: 0, y: -200 },  // Line 1 (up)
        { x: 200, y: 0 },   // Line 2 (right)
        { x: 0, y: 200 },   // Line 3 (down)
        { x: -200, y: 0 }   // Line 4 (left)
    ];

    mainProfile.addEventListener('mouseenter', () => {
        studentProfiles.forEach((profile, index) => {
            profile.style.opacity = '1';
            profile.style.transform = `translate(${linesCoords[index].x}px, ${linesCoords[index].y}px)`;
        });

        lines.forEach((line, index) => {
            line.style.transform = 'scaleY(1)';
        });
    });

    mainProfile.addEventListener('mouseleave', () => {
        studentProfiles.forEach(profile => {
            profile.style.opacity = '0';
            profile.style.transform = 'translate(0, 0)';
        });

        lines.forEach(line => {
            line.style.transform = 'scaleY(0)';
        });
    });

    container.addEventListener('mousemove', (event) => {
        const rect = container.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const angleStep = (2 * Math.PI) / studentProfiles.length;

        studentProfiles.forEach((profile, index) => {
            const angle = angleStep * index;
            const offsetX = 200 * Math.cos(angle);
            const offsetY = 200 * Math.sin(angle);

            profile.style.left = `${centerX + offsetX}px`;
            profile.style.top = `${centerY + offsetY}px`;

            lines[index].style.transform = `translate(${centerX + offsetX}px, ${centerY + offsetY}px)`;
        });
    });
});
