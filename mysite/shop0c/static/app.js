(() => {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const numberFormat = new Intl.NumberFormat("ja-JP");

  const showToast = (message, tone = "success") => {
    let stack = document.querySelector("[data-toast-stack]");
    if (!stack) {
      stack = document.createElement("div");
      stack.className = "toast-stack";
      stack.dataset.toastStack = "";
      document.body.appendChild(stack);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast--${tone}`;
    toast.setAttribute("role", "status");
    toast.textContent = message;
    stack.appendChild(toast);

    window.setTimeout(() => {
      toast.classList.add("is-hiding");
      toast.addEventListener("transitionend", () => toast.remove(), { once: true });
    }, 2600);
  };

  const initPage = () => {
    if (reducedMotion) return;
    document.body.classList.add("page-enter");
    requestAnimationFrame(() => document.body.classList.add("is-ready"));
  };

  const initPointerAura = () => {
    if (reducedMotion || !window.matchMedia("(pointer: fine)").matches) return;
    window.addEventListener("pointermove", (event) => {
      document.body.style.setProperty("--pointer-x", `${event.clientX}px`);
      document.body.style.setProperty("--pointer-y", `${event.clientY}px`);
    }, { passive: true });
  };

  const initHeader = () => {
    const headers = document.querySelectorAll(".site-header, .admin-header");
    if (!headers.length) return;

    const progress = document.createElement("div");
    progress.className = "scroll-progress";
    progress.setAttribute("aria-hidden", "true");
    document.body.appendChild(progress);

    const update = () => {
      headers.forEach((header) => header.classList.toggle("is-scrolled", window.scrollY > 8));
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? Math.min(window.scrollY / max, 1) : 0})`;
    };

    update();
    window.addEventListener("scroll", update, { passive: true });
  };

  const initHero = () => {
    const hero = document.querySelector(".hero");
    if (!hero || reducedMotion) return;

    hero.addEventListener("pointermove", (event) => {
      const rect = hero.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      hero.style.setProperty("--hero-x", x.toFixed(3));
      hero.style.setProperty("--hero-y", y.toFixed(3));
    }, { passive: true });
  };

  const initMobileNav = () => {
    const toggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.classList.toggle("is-open", isOpen);
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "メニューを閉じる" : "メニューを開く");
    });
  };

  const initReveal = () => {
    const targets = document.querySelectorAll(
      ".hero, .search-box, .section-head, .product-card, .card, .page-actions, .page-links"
    );

    targets.forEach((target, index) => {
      target.classList.add("reveal");
      target.style.setProperty("--reveal-delay", `${Math.min(index * 55, 420)}ms`);
    });

    if (reducedMotion || !("IntersectionObserver" in window)) {
      targets.forEach((target) => target.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -24px" });

    targets.forEach((target) => observer.observe(target));
  };

  const initTilt = () => {
    if (reducedMotion || !window.matchMedia("(pointer: fine)").matches) return;

    document.querySelectorAll(".product-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = ((event.clientX - rect.left) / rect.width - 0.5) * 8;
        const y = ((event.clientY - rect.top) / rect.height - 0.5) * -8;
        card.style.transform = `translateY(-8px) rotateX(${y}deg) rotateY(${x}deg)`;
      }, { passive: true });

      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  };

  const initNumbers = () => {
    if (reducedMotion) return;

    document.querySelectorAll(".product-card__price, .price__num, .cart-total .num").forEach((target) => {
      const raw = target.textContent.replace(/[^\d]/g, "");
      const finalValue = Number(raw);
      if (!finalValue) return;

      const hasYen = target.textContent.includes("¥");
      const start = performance.now();
      const duration = 850;

      const tick = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        target.textContent = `${hasYen ? "¥" : ""}${numberFormat.format(Math.round(finalValue * eased))}`;
        if (progress < 1) requestAnimationFrame(tick);
      };

      requestAnimationFrame(tick);
    });
  };

  const initRipple = () => {
    if (reducedMotion) return;

    document.querySelectorAll("button, .btn-primary, a.link-btn").forEach((control) => {
      control.classList.add("has-ripple");
      control.addEventListener("pointerdown", (event) => {
        const rect = control.getBoundingClientRect();
        const ripple = document.createElement("span");
        const size = Math.max(rect.width, rect.height);
        ripple.className = "ripple";
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
        control.appendChild(ripple);
        ripple.addEventListener("animationend", () => ripple.remove(), { once: true });
      });
    });
  };

  const initActiveNav = () => {
    const current = window.location.pathname.replace(/\/$/, "");
    document.querySelectorAll(".navbar-menu a, .admin-nav a").forEach((link) => {
      const path = new URL(link.href, window.location.origin).pathname.replace(/\/$/, "");
      link.classList.toggle("is-active", path === current);
    });
  };

  const initSearchFeedback = () => {
    document.querySelectorAll(".search-box form, .admin-search form").forEach((form) => {
      const keyword = form.querySelector('input[name="keyword"]');
      const submit = form.querySelector('button[type="submit"], input[type="submit"]');
      if (!keyword || !submit) return;

      const hint = document.createElement("p");
      hint.className = "form-hint";
      hint.setAttribute("aria-live", "polite");
      keyword.insertAdjacentElement("afterend", hint);

      const update = () => {
        const value = keyword.value.trim();
        hint.textContent = value ? `"${value}" で探します` : "キーワードなしでも探せます";
        submit.classList.toggle("is-ready", Boolean(value));
      };

      update();
      keyword.addEventListener("input", update);
    });
  };

  const initCartTotal = () => {
    const table = document.querySelector(".cart-table");
    const total = document.querySelector(".cart-total .num");
    if (!table || !total) return;

    let sum = 0;
    table.querySelectorAll("tr").forEach((row) => {
      const cells = row.querySelectorAll("td");
      if (cells.length < 4) return;
      const price = Number(cells[2].textContent.replace(/[^\d]/g, "")) || 0;
      const amount = Number(cells[3].textContent.replace(/[^\d]/g, "")) || 0;
      sum += price * amount;
    });

    total.textContent = numberFormat.format(sum);
    total.classList.add("is-bumped");
    window.setTimeout(() => total.classList.remove("is-bumped"), 260);
  };

  const initConfirmations = () => {
    document.querySelectorAll('input[value="削除"], input[value="退会"], input[value="キャンセルする"]').forEach((button) => {
      const form = button.closest("form");
      if (!form) return;

      form.addEventListener("submit", (event) => {
        if (form.dataset.confirmed === "true") return;
        if (window.confirm("この操作を実行しますか？")) {
          form.dataset.confirmed = "true";
          return;
        }

        event.preventDefault();
        event.stopImmediatePropagation();
        button.classList.remove("is-loading");
        showToast("操作を取り消しました", "neutral");
      });
    });
  };

  const initForms = () => {
    document.querySelectorAll("form").forEach((form) => {
      form.addEventListener("submit", (event) => {
        const submitter = event.submitter;
        const label = submitter?.value || submitter?.textContent || "";
        if (submitter && !label.includes("削除")) {
          submitter.classList.add("is-loading");
        }
        if (submitter?.classList.contains("btn-cart")) {
          showToast("カートへ進みます");
        }
      });
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    initPage();
    initPointerAura();
    initHeader();
    initHero();
    initMobileNav();
    initReveal();
    initTilt();
    initNumbers();
    initRipple();
    initActiveNav();
    initSearchFeedback();
    initCartTotal();
    initConfirmations();
    initForms();
  });
})();
