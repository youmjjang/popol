(() => {
  const menuButton = document.querySelector('#menuToggle');
  const nav = document.querySelector('#nav');
  if (menuButton && nav) {
    const closeMenu = () => { nav.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', '메뉴 열기'); };
    menuButton.addEventListener('click', () => {
      const opened = nav.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(opened));
      menuButton.setAttribute('aria-label', opened ? '메뉴 닫기' : '메뉴 열기');
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    window.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 850) closeMenu(); });
  }
})();