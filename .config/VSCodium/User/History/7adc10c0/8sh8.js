document.addEventListener('DOMContentLoaded', () => {
    const mainProfile = document.getElementById('mainProfile');
    const studentProfiles = document.querySelectorAll('.student-profile');
    const lines = document.querySelectorAll('line');
    const container = document.querySelector('.container');

    const positions = [
        { x: 0, y: -200 },  // Top
        { x: 200, y: 0 },   // Right
        { x: 0, y: 200 },   // Bottom
        { x: -200, y: 0 }   // Left
    ];

    mainProfile.addEventListener('mouseenter', () => {
        studentProfiles.forEach((profile, index) => {
            profile.style.opacity = '1';
            const { x, y } = positions[index];
            profile.style.transform = `translate(${x}px, ${y}px)`;
            updateLine(lines[index], mainProfile, profile);
        });
    });

    mainProfile.addEventListener('mouseleave', () => {
        studentProfiles.forEach(profile => {
            profile.style.opacity = '0';
            profile.style.transform = 'translate(0, 0)';
        });

        lines.forEach(line => {
            line.setAttribute('x2', '50%');
            line.setAttribute('y2', '50%');
        });
    });

    function updateLine(line, mainProfile, studentProfile) {
        const mainRect = mainProfile.getBoundingClientRect();
        const studentRect = studentProfile.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const x1 = mainRect.left + mainRect.width / 2 - containerRect.left;
        const y1 = mainRect.top + mainRect.height / 2 - containerRect.top;

        const x2 = studentRect.left + studentRect.width / 2 - containerRect.left;
        const y2 = studentRect.top + studentRect.height / 2 - containerRect.top;

        line.setAttribute('x1', `${x1}`);
        line.setAttribute('y1', `${y1}`);
        line.setAttribute('x2', `${x2}`);
        line.setAttribute('y2', `${y2}`);
    }

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

            updateLine(lines[index], mainProfile, profile);
        });
    });
});
