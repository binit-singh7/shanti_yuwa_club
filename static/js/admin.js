document.addEventListener('DOMContentLoaded', function () {
	// Elements
	const sidebar = document.getElementById('adminSidebar');
	const main = document.getElementById('adminMain');
	const toggleBtn = document.getElementById('sidebarToggle');
	const mobileClose = document.getElementById('mobileSidebarClose');

	function setSidebarExpanded(expanded) {
		if (!sidebar || !main) return;
		console.log('[admin] setSidebarExpanded ->', expanded);
		if (expanded) {
			sidebar.classList.add('expanded');
			main.classList.add('expanded');
		} else {
			sidebar.classList.remove('expanded');
			main.classList.remove('expanded');
		}
		// set aria state on the toggle for accessibility
		if (toggleBtn) toggleBtn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
		localStorage.setItem('adminSidebarExpanded', expanded ? 'true' : 'false');
	}

	// Initialize from storage (support older collapsed key too). Ensure a deterministic initial state.
	try {
		console.log('[admin] initializing sidebar state from localStorage');
		const expandedStored = localStorage.getItem('adminSidebarExpanded');
		const collapsedStored = localStorage.getItem('adminSidebarCollapsed');
		if (expandedStored === 'true') setSidebarExpanded(true);
		else if (collapsedStored === 'true') setSidebarExpanded(false);
		else setSidebarExpanded(false); // default to collapsed for clarity
	} catch (e) {
		console.warn('[admin] localStorage unavailable, defaulting sidebar to collapsed');
		setSidebarExpanded(false);
	}

	// Toggle handler
	if (toggleBtn) {
		toggleBtn.addEventListener('click', function () {
			const expanded = sidebar.classList.contains('expanded');
			console.log('[admin] sidebar toggle clicked. currentExpanded=', expanded);
			setSidebarExpanded(!expanded);
		});
		// ensure aria-expanded attribute reflects current state
		if (sidebar.classList.contains('expanded')) toggleBtn.setAttribute('aria-expanded', 'true');
		else toggleBtn.setAttribute('aria-expanded', 'false');
	}
	if (mobileClose) {
		mobileClose.classList.remove('hidden');
		mobileClose.addEventListener('click', function () {
			setSidebarExpanded(false);
		});
	}

	// Wire search input to admin search
	const searchInput = document.querySelector('.search-input');
	if (searchInput) {
		searchInput.addEventListener('keydown', function (e) {
			if (e.key === 'Enter') {
				const q = searchInput.value.trim();
				if (q.length) {
					window.location.href = '/admin/?q=' + encodeURIComponent(q);
				}
			}
		});
	}


	// Dismissible messages
	document.querySelectorAll('.message-close').forEach(btn => {
		btn.addEventListener('click', function () {
			const parent = btn.closest('.alert');
			if (parent) parent.remove();
		});
	});

	// Auto-hide messages after 6s
	document.querySelectorAll('.alert').forEach(alert => {
		setTimeout(() => {
			alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
			alert.style.opacity = '0';
			alert.style.transform = 'translateY(-6px)';
			setTimeout(() => {
				if (alert.parentNode) alert.parentNode.removeChild(alert);
			}, 350);
		}, 6000);
	});

	// Sidebar active state (graceful)
	const currentUrl = window.location.pathname;
	document.querySelectorAll('.nav-item').forEach(item => {
		try {
			const href = item.getAttribute('href');
			if (href && href === currentUrl) {
				item.classList.add('active');
			} else {
				item.classList.remove('active');
			}
		} catch (err) {}
	});

    // Notifications & user menu toggles
    const notifToggle = document.getElementById('notifToggle');
    const notifDropdown = document.getElementById('notifDropdown');
    const userToggle = document.getElementById('userToggle');
    const userDropdown = document.getElementById('userDropdown');

    function closeAllMenus(){
        if(notifDropdown) notifDropdown.classList.add('hidden');
        if(userDropdown) userDropdown.classList.add('hidden');
    }

    if(notifToggle && notifDropdown){
        notifToggle.addEventListener('click', function(e){
            e.stopPropagation();
            notifDropdown.classList.toggle('hidden');
            if(userDropdown) userDropdown.classList.add('hidden');

        });
    }
    if(userToggle && userDropdown){
        userToggle.addEventListener('click', function(e){
            e.stopPropagation();
            userDropdown.classList.toggle('hidden');
            if(notifDropdown) notifDropdown.classList.add('hidden');

        });
    }



    document.addEventListener('click', function(){ closeAllMenus(); });

});
