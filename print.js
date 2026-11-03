(() => {
  const pages = [...document.querySelectorAll('.sheet')];
  const current = document.getElementById('currentPage');
  let active = 0;
  const setActive = index => {
    active = Math.min(Math.max(index, 0), pages.length - 1);
    if (current) current.textContent = String(active + 1).padStart(2, '0');
  };
  document.getElementById('prevPage')?.addEventListener('click', () => {
    setActive(active - 1);
    pages[active]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  document.getElementById('nextPage')?.addEventListener('click', () => {
    setActive(active + 1);
    pages[active]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  document.getElementById('printButton')?.addEventListener('click', () => window.print());
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(item => item.isIntersecting).sort((a,b)=>b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) setActive(pages.indexOf(visible[0].target));
    }, { rootMargin: '-15% 0px -30% 0px', threshold: [.1, .25, .5, .75] });
    pages.forEach(page => observer.observe(page));
  }
})();