document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.querySelector('[data-autocomplete]');
    if (searchInput) {
        initAutocomplete(searchInput);
    }

    var lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('loading');
                    observer.unobserve(img);
                }
            });
        });
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    } else {
        lazyImages.forEach(function(img) {
            img.src = img.dataset.src;
        });
    }

    var viewCountElements = document.querySelectorAll('[data-view-count]');
    viewCountElements.forEach(function(el) {
        el.textContent = formatNumber(parseInt(el.dataset.viewCount) || 0);
    });
});

function initAutocomplete(input) {
    var container = document.createElement('div');
    container.className = 'autocomplete-dropdown';
    container.style.cssText = 'position:absolute;top:100%;left:0;right:0;background:#fff;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:1000;display:none;max-height:300px;overflow-y:auto;margin-top:4px;';
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(container);

    var debounceTimer;
    input.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        var query = input.value.trim();
        if (query.length < 2) {
            container.style.display = 'none';
            return;
        }
        debounceTimer = setTimeout(function() {
            fetch('/api/autocomplete/?q=' + encodeURIComponent(query))
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    if (data.suggestions && data.suggestions.length > 0) {
                        container.innerHTML = '';
                        data.suggestions.forEach(function(s) {
                            var item = document.createElement('div');
                            item.style.cssText = 'padding:10px 16px;cursor:pointer;border-bottom:1px solid #f0f0f0;transition:background 0.2s;';
                            item.textContent = s;
                            item.addEventListener('mouseenter', function() {
                                item.style.background = '#f8f5f0';
                            });
                            item.addEventListener('mouseleave', function() {
                                item.style.background = 'transparent';
                            });
                            item.addEventListener('click', function() {
                                input.value = s;
                                container.style.display = 'none';
                                input.closest('form').submit();
                            });
                            container.appendChild(item);
                        });
                        container.style.display = 'block';
                    } else {
                        container.style.display = 'none';
                    }
                });
        }, 200);
    });

    input.addEventListener('focus', function() {
        if (input.value.trim().length >= 2) {
            input.dispatchEvent(new Event('input'));
        }
    });

    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !container.contains(e.target)) {
            container.style.display = 'none';
        }
    });
}

function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toString();
}
