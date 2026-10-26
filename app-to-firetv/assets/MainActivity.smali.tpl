.class public L__PKGPATH__/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"

.field private webView:Landroid/webkit/WebView;

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 6
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    invoke-virtual {p0}, L__PKGPATH__/MainActivity;->getWindow()Landroid/view/Window;
    move-result-object v0
    const/16 v1, 0x480
    invoke-virtual {v0, v1}, Landroid/view/Window;->addFlags(I)V

    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    const/high16 v1, -0x1000000
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setBackgroundColor(I)V

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    const/4 v3, 0x0
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setMediaPlaybackRequiresUserGesture(Z)V

    new-instance v1, L__PKGPATH__/MainActivity$Client;
    invoke-direct {v1, p0}, L__PKGPATH__/MainActivity$Client;-><init>(L__PKGPATH__/MainActivity;)V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    invoke-virtual {v0, v2}, Landroid/view/View;->setFocusable(Z)V
    invoke-virtual {v0, v2}, Landroid/view/View;->setFocusableInTouchMode(Z)V
    invoke-virtual {p0, v0}, L__PKGPATH__/MainActivity;->setContentView(Landroid/view/View;)V
    invoke-virtual {v0}, Landroid/view/View;->requestFocus()Z
    const-string v1, "file:///android_asset/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    return-void
.end method

.method public dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    .registers 6
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I
    move-result v0
    const/16 v1, 0x13
    if-eq v0, v1, :up
    const/16 v1, 0x14
    if-eq v0, v1, :down
    const/16 v1, 0x15
    if-eq v0, v1, :left
    const/16 v1, 0x16
    if-eq v0, v1, :right
    const/16 v1, 0x17
    if-eq v0, v1, :select
    const/16 v1, 0x42
    if-eq v0, v1, :select
    const/16 v1, 0xa0
    if-eq v0, v1, :select
    const/4 v1, 0x4
    if-eq v0, v1, :back
    const/16 v1, 0x6f
    if-eq v0, v1, :back
    const/16 v1, 0x52
    if-eq v0, v1, :menu
    const/16 v1, 0x55
    if-eq v0, v1, :play
    const/16 v1, 0x7e
    if-eq v0, v1, :play
    const/16 v1, 0x7f
    if-eq v0, v1, :play
    const/16 v1, 0x59
    if-eq v0, v1, :rew
    const/16 v1, 0x5a
    if-eq v0, v1, :ff
    invoke-super {p0, p1}, Landroid/app/Activity;->dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    move-result v0
    return v0
    :up
    const-string v2, "UP"
    goto :send
    :down
    const-string v2, "DOWN"
    goto :send
    :left
    const-string v2, "LEFT"
    goto :send
    :right
    const-string v2, "RIGHT"
    goto :send
    :select
    const-string v2, "SELECT"
    goto :send
    :back
    const-string v2, "BACK"
    goto :send
    :menu
    const-string v2, "MENU"
    goto :send
    :rew
    const-string v2, "REWIND"
    goto :send
    :ff
    const-string v2, "FAST_FORWARD"
    goto :send
    :play
    const-string v2, "PLAY_PAUSE"
    :send
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :done
    iget-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    if-eqz v0, :done
    new-instance v1, Ljava/lang/StringBuilder;
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V
    const-string v3, "window.fireTvKey && window.fireTvKey('"
    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v3, "');"
    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    const/4 v3, 0x0
    invoke-virtual {v0, v1, v3}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    :done
    const/4 v0, 0x1
    return v0
.end method

.method protected onPause()V
    .registers 2
    invoke-super {p0}, Landroid/app/Activity;->onPause()V
    iget-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    if-eqz v0, :end
    invoke-virtual {v0}, Landroid/webkit/WebView;->onPause()V
    :end
    return-void
.end method

.method protected onResume()V
    .registers 2
    invoke-super {p0}, Landroid/app/Activity;->onResume()V
    iget-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    if-eqz v0, :end
    invoke-virtual {v0}, Landroid/webkit/WebView;->onResume()V
    :end
    return-void
.end method

.method protected onDestroy()V
    .registers 2
    iget-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    if-eqz v0, :end
    invoke-virtual {v0}, Landroid/webkit/WebView;->destroy()V
    const/4 v0, 0x0
    iput-object v0, p0, L__PKGPATH__/MainActivity;->webView:Landroid/webkit/WebView;
    :end
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V
    return-void
.end method
