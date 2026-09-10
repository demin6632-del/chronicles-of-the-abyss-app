package com.pokoritel.bashni;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        WebView webView = new WebView(this);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                String scheme = request != null && request.getUrl() != null
                        ? request.getUrl().getScheme()
                        : null;

                // Игра должна работать автономно: блокируем внешние HTTP/HTTPS-запросы.
                if (scheme != null && ("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme))) {
                    return new WebResourceResponse("text/plain", "UTF-8", null);
                }

                return super.shouldInterceptRequest(view, request);
            }
        });

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(false);
        settings.setDatabaseEnabled(true);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setSupportZoom(false);

        // localStorage находится в данных приложения и сохраняется при обычном обновлении APK.
        webView.loadUrl("file:///android_asset/game.html");
        setContentView(webView);
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        // Не закрываем игру случайным нажатием системной кнопки "Назад".
        // Навигация внутри игры управляется самой HTML-игрой.
        if (isFinishing()) {
            return;
        }
    }
}
