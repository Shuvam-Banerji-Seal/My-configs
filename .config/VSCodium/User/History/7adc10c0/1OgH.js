document.addEventListener('DOMContentLoaded', () => {
    const mainProfile = document.getElementById('mainProfile');
    const studentProfiles = document.querySelectorAll('.student-profile');
    const paths = document.querySelectorAll('path');
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
            updatePath(paths[index], mainProfile, profile);
        });

        paths.forEach((path) => {
            path.style.strokeDasharray = '200';
            path.style.strokeDashoffset = '0';
        });
    });

    mainProfile.addEventListener('mouseleave', () => {
        studentProfiles.forEach(profile => {
            profile.style.opacity = '0';
            profile.style.transform = 'translate(0, 0)';
        });

        paths.forEach((path) => {
            path.style.strokeDasharray = '200';
            path.style.strokeDashoffset = '200';
        });
    });

    function updatePath(path, mainProfile, studentProfile) {
        const mainRect = mainProfile.getBoundingClientRect();
        const studentRect = studentProfile.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const x1 = mainRect.left + mainRect.width / 2 - containerRect.left;
        const y1 = mainRect.top + mainRect.height / 2 - containerRect.top;

        const x2 = studentRect.left + studentRect.width / 2 - containerRect.left;
        const y2 = studentRect.top + studentRect.height / 2 - containerRect.top;

        const radius = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)) / 2;
        const arcPath = `M${x1},${y1} A${radius},${radius} 0 0,1 ${x2},${y2}`;
        path.setAttribute('d', arcPath);
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

            updatePath(paths[index], mainProfile, profile);
        });
    });
});
