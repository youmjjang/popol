// Small, dependency-free interactions. No analytics or tracking.
const menu = document.querySelector('#menu');
const nav = document.querySelector('#nav');
if (menu && nav) {
  menu.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') === 'true';
    menu.setAttribute('aria-expanded', String(!expanded));
    menu.setAttribute('aria-label', expanded ? '메뉴 열기' : '메뉴 닫기');
    nav.classList.toggle('open', !expanded);
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', '메뉴 열기');
  }));
}
const filters = document.querySelectorAll('.filter');
const projects = document.querySelectorAll('.project');
filters.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  filters.forEach(filter => {
    const selected = filter === button;
    filter.classList.toggle('selected', selected);
    filter.setAttribute('aria-pressed', String(selected));
  });
  projects.forEach(project => {
    project.hidden = category !== 'all' && !project.dataset.category.split(' ').includes(category);
  });
}));
