/* ==========================================
   Zensical-Wcowin 自定义脚本
   ========================================== */

function getSharePayload() {
  return {
    title: document.querySelector("h1")?.textContent?.trim() || document.title,
    url: window.location.href.split("#")[0],
  };
}

async function copyShareText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const input = document.createElement("textarea");
  input.value = text;
  input.setAttribute("readonly", "");
  input.style.position = "fixed";
  input.style.opacity = "0";
  document.body.appendChild(input);
  input.select();
  document.execCommand("copy");
  input.remove();
}

function showShareToast(message) {
  document.querySelectorAll(".post-share-toast").forEach((toast) => toast.remove());

  const toast = document.createElement("div");
  toast.className = "post-share-toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add("post-share-toast--visible");
  });

  setTimeout(() => {
    toast.classList.remove("post-share-toast--visible");
    setTimeout(() => toast.remove(), 200);
  }, 3000);
}

function setupPostShare() {
  const container = document.querySelector(".post-share");
  if (!container) {
    return;
  }

  const payload = getSharePayload();
  const shareText = `${payload.title}\n${payload.url}`;
  const xLink = container.querySelector("[data-share-x]");

  if (xLink) {
    const params = new URLSearchParams({
      text: payload.title,
      url: payload.url,
    });
    xLink.href = `https://twitter.com/intent/tweet?${params.toString()}`;
  }

  const weiboLink = container.querySelector("[data-share-weibo]");
  if (weiboLink) {
    const params = new URLSearchParams({
      title: payload.title,
      url: payload.url,
    });
    weiboLink.href = `https://service.weibo.com/share/share.php?${params.toString()}`;
  }

  container.querySelectorAll("[data-share-wechat]").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        await copyShareText(shareText);
        showShareToast("标题和链接已复制，请前往微信或公众号后台粘贴分享。");
      } catch (error) {
        showShareToast("复制失败，请手动复制地址栏链接。");
      }
    });
  });
}

// 即时导航兼容
document$.subscribe(function() {
  console.log("SWHL loaded");

  // 在这里添加你的自定义 JavaScript
  setupPostShare();
});
