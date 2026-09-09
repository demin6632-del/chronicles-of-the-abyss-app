package com.chroniclesoftheabyss.app;

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
                String scheme = request.getUrl().getScheme();
                if (scheme != null) {
                    scheme = scheme.toLowerCase();
                    if (scheme.equals("http") || scheme.equals("https")) {
                        return new WebResourceResponse("text/plain", "UTF-8", null);
                    }
                }
                return super.shouldInterceptRequest(view, request);
            }
        });

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        webView.loadUrl("file:///android_asset/game.html");
        setContentView(webView);
    }

    @Override
    public void onBackPressed() {
        // Игра работает как самостоятельное приложение; системная кнопка «Назад» не закрывает её случайно.
    }
}
