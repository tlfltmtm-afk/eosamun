const CACHE_NAME = 'eosamun-cache-v33';
const FILES_TO_CACHE = [
  '/',
  '/index.html',
  '/serial-order.html',
  '/hanja-sound.html',
  '/vocabulary.html',
  '/search.html'
  // 참고: '/manifest.json', '/icon-192.png' 등 앱의 핵심 자산도 추가하면 좋습니다.
];

// 서비스 워커 설치 단계: 지정된 파일을 캐시에 저장합니다.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// 서비스 워커 활성화 및 오래된 캐시 정리 단계
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[Service Worker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
});

// 데이터 요청 시 캐시에서 먼저 찾아보고, 없으면 네트워크로 요청
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});