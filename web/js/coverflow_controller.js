/**
 * 3D Cover Flow Controller (Premium v1.34)
 * Handles high-end 3D transitions, keyboard/mouse wheel navigation, and centering logic.
 */

class Coverflow {
    constructor(containerId, trackId) {
        this.container = document.getElementById(containerId);
        this.track = document.getElementById(trackId);
        this.items = [];
        this.activeIndex = 0;
        this.spacing = 150; // Distance between focused and sidebar items
        this.tilt = 45;     // Angle of rotated items
        this.isAnimating = false;

        this.initEvents();
    }

    setItems(data) {
        this.items = data || [];
        this.render();
    }

    initEvents() {
        if (!this.container) return;

        // Mouse Wheel (Horizontal/Vertical scroll)
        this.container.onwheel = (e) => {
            e.preventDefault();
            if (this.isAnimating) return;
            if (e.deltaY > 0 || e.deltaX > 0) this.next();
            else this.prev();
        };

        // Keyboard Navigation (Global if Library is active)
        window.addEventListener('keydown', (e) => {
            const activeTab = localStorage.getItem('mwv_active_tab');
            if (activeTab !== 'library') return;

            if (e.key === 'ArrowRight') this.next();
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'Enter') {
                const activeItem = this.items[this.activeIndex];
                if (activeItem && typeof handleCoverSelect === 'function') handleCoverSelect(activeItem);
            }
        });
    }

    next() {
        if (this.activeIndex < this.items.length - 1) {
            this.activeIndex++;
            this.update();
        }
    }

    prev() {
        if (this.activeIndex > 0) {
            this.activeIndex--;
            this.update();
        }
    }

    render() {
        if (!this.track) return;
        this.track.innerHTML = ''; // Clear existing

        this.items.forEach((item, index) => {
            const el = document.createElement('div');
            el.className = 'cover_flow_item';
            el.id = `cover-flow-node-${index}`;
            el.style.backgroundImage = `url('/cover/${encodeURIComponent(item.name)}')`;
            
            // Info Overlay (Subtle)
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: absolute; bottom: 0; left: 0; right: 0; padding: 15px;
                background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 100%);
                border-radius: 0 0 var(--radius-card) var(--radius-card); opacity: 0;
                transition: opacity 0.3s ease; display: flex; flex-direction: column;
            `;
            overlay.innerHTML = `
                <strong style="color: white; font-size: 13px;">${item.tags?.title || item.name}</strong>
                <span style="color: #aaa; font-size: 11px;">${item.tags?.artist || 'Unknown'}</span>
            `;
            el.appendChild(overlay);
            el.dataset.overlay = 'true';

            // Reflection
            const reflection = document.createElement('div');
            reflection.className = 'reflection';
            el.appendChild(reflection);

            el.onclick = (e) => {
                if (index === this.activeIndex) {
                    if (typeof handleCoverSelect === 'function') handleCoverSelect(item);
                } else {
                    this.activeIndex = index;
                    this.update();
                }
            };

            this.track.appendChild(el);
        });

        this.update();
    }

    update() {
        if (this.isAnimating) return;
        this.isAnimating = true;

        const containerHalfWidth = this.container.offsetWidth / 2;
        const itemWidth = 280;

        Array.from(this.track.children).forEach((el, index) => {
            const distance = index - this.activeIndex;
            const absDistance = Math.abs(distance);
            
            let translateX = distance * this.spacing;
            let rotateY = 0;
            let translateZ = 0;
            let opacity = 1;
            let zIndex = 100 - absDistance;

            if (distance < 0) {
                // To the Left
                rotateY = this.tilt;
                translateX -= (itemWidth / 2);
                translateZ = -absDistance * 100;
            } else if (distance > 0) {
                // To the Right
                rotateY = -this.tilt;
                translateX += (itemWidth / 2);
                translateZ = -absDistance * 100;
            } else {
                // Center Focus
                translateZ = 150;
                el.classList.add('active');
                if (el.children[0]) el.children[0].style.opacity = '1';
            }

            if (absDistance === 0) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
                if (el.children[0]) el.children[0].style.opacity = '0';
            }

            // High-density scaling
            if (absDistance > 3) opacity = Math.max(0, 1 - (absDistance - 3) * 0.3);

            el.style.transform = `translateX(${translateX}px) rotateY(${rotateY}deg) translateZ(${translateZ}px)`;
            el.style.zIndex = zIndex;
            el.style.opacity = opacity;
        });

        setTimeout(() => { this.isAnimating = false; }, 500);
    }
}

// Global instantiation helper
window.initCoverflow = (data) => {
    if (!window.mwv_coverflow) {
        window.mwv_coverflow = new Coverflow('coverflow-container', 'coverflow-track');
    }
    window.mwv_coverflow.setItems(data);
};

// Selection handler
function handleCoverSelect(item) {
    console.log("[CoverFlow] Selected:", item.name);
    if (typeof mwv_trace === 'function') mwv_trace('UI-INPUT', 'COVERFLOW-SELECT', { name: item.name });
    
    if (typeof playAudio === 'function' && (item.type === 'audio' || item.category === 'Music')) {
        playAudio(item);
        switchTab('player');
    } else if (typeof playVideo === 'function' && item.type === 'video') {
        playVideo(item);
        switchTab('video');
    }
}

// Created with MWV v1.46.00-MASTER
