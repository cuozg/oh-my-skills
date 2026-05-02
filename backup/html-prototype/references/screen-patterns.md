# Common App Screen Patterns

This document provides a collection of semantic HTML and CSS patterns for common screens found in mobile and web applications. These patterns are designed to be used as structural starting points for interactive prototypes.

## Table of Contents
1. [Splash Screen](#splash-screen)
2. [Login Screen](#login-screen)
3. [Register Screen](#register-screen)
4. [Home/Dashboard](#home-dashboard)
5. [List Screen](#list-screen)
6. [Detail Screen](#detail-screen)
7. [Settings Screen](#settings-screen)
8. [Profile Screen](#profile-screen)
9. [Onboarding](#onboarding)
10. [Modal/Bottom Sheet](#modal-bottom-sheet)
11. [Search Screen](#search-screen)
12. [Empty State](#empty-state)
13. [Tab Bar Layout](#tab-bar-layout)

---

## Splash Screen
App logo and name centered. Features a fade-in animation and auto-navigation logic.

```html
<section class="screen splash-screen" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: var(--surface); animation: fadeIn 0.8s ease-out;">
  <div class="logo-container" style="width: 120px; height: 120px; background: var(--primary); border-radius: 24px; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
    <!-- inject: app.logo_svg -->
    <div style="width: 60px; height: 60px; background: white; border-radius: 12px;"></div>
  </div>
  <h1 style="color: var(--text); font-size: 32px; font-weight: 700;">
    <!-- inject: app.name -->
    App Prototype
  </h1>
  
  <script>
    // Pattern logic: Auto-navigates after 1.5s
    setTimeout(() => navigateTo('login'), 1500);
  </script>
</section>
```

---

## Login Screen
Clean centered layout with email/password inputs and recovery links.

```html
<section class="screen login-screen" style="padding: 40px 24px; display: flex; flex-direction: column; align-items: stretch; justify-content: center; min-height: 100vh; background: var(--surface);">
  <div style="text-align: center; margin-bottom: 48px;">
    <div style="width: 80px; height: 80px; background: var(--primary); border-radius: 16px; margin: 0 auto 16px; display: flex; align-items: center; justify-content: center;"></div>
    <h2 style="font-size: 24px; color: var(--text);">Welcome Back</h2>
    <p style="color: var(--text-muted);">Sign in to continue</p>
  </div>

  <form onsubmit="event.preventDefault(); navigateTo('home')" style="display: flex; flex-direction: column; gap: 16px;">
    <div class="input-group">
      <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500;">Email</label>
      <input type="email" placeholder="hello@example.com" required style="width: 100%; height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    </div>
    
    <div class="input-group">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <label style="font-size: 14px; font-weight: 500;">Password</label>
        <a href="#" onclick="navigateTo('forgot-password')" style="color: var(--primary); font-size: 14px; text-decoration: none;">Forgot?</a>
      </div>
      <input type="password" placeholder="••••••••" required style="width: 100%; height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    </div>

    <button type="submit" style="height: 52px; background: var(--primary); color: white; border: none; border-radius: 12px; font-weight: 600; font-size: 16px; margin-top: 12px; cursor: pointer;">Sign In</button>
  </form>

  <div style="text-align: center; margin-top: 32px;">
    <p style="color: var(--text-muted); font-size: 14px;">
      Don't have an account? 
      <a href="#" onclick="navigateTo('register')" style="color: var(--primary); font-weight: 600; text-decoration: none;">Create account</a>
    </p>
  </div>
</section>
```

---

## Register Screen
Onboarding flow for new users with confirmation fields.

```html
<section class="screen register-screen" style="padding: 40px 24px; background: var(--surface); min-height: 100vh;">
  <button onclick="navigateTo('login')" style="background: none; border: none; padding: 8px 0; color: var(--text); display: flex; align-items: center; gap: 8px; margin-bottom: 32px;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
    Back
  </button>

  <h2 style="font-size: 28px; margin-bottom: 8px; color: var(--text);">Create Account</h2>
  <p style="color: var(--text-muted); margin-bottom: 32px;">Join us to start your journey</p>

  <form onsubmit="event.preventDefault(); navigateTo('home')" style="display: flex; flex-direction: column; gap: 16px;">
    <input type="text" placeholder="Full Name" style="height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    <input type="email" placeholder="Email Address" style="height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    <input type="password" placeholder="Password" style="height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    <input type="password" placeholder="Confirm Password" style="height: 48px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">

    <button type="submit" style="height: 52px; background: var(--primary); color: white; border: none; border-radius: 12px; font-weight: 600; font-size: 16px; margin-top: 12px;">Create Account</button>
  </form>
</section>
```

---

## Home/Dashboard
Main app hub with personalized greeting and overview cards.

```html
<section class="screen home-screen" style="background: var(--surface-alt); min-height: 100vh;">
  <header style="padding: 24px; background: var(--surface); border-bottom: 1px solid var(--border);">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <p style="color: var(--text-muted); font-size: 14px; margin: 0;">Good morning,</p>
        <h2 style="font-size: 20px; margin: 4px 0 0; color: var(--text);">
          <!-- inject: user.first_name -->
          Sarah Jones
        </h2>
      </div>
      <div onclick="navigateTo('profile')" style="width: 44px; height: 44px; border-radius: 22px; background: var(--primary-light); overflow: hidden;">
        <!-- inject: user.avatar_img -->
        <div style="width: 100%; height: 100%; background: var(--primary);"></div>
      </div>
    </div>
  </header>

  <div class="content" style="padding: 24px; display: flex; flex-direction: column; gap: 24px;">
    <!-- Summary Cards -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
      <div style="background: var(--surface); padding: 16px; border-radius: 16px; box-shadow: 0 2px 8px var(--shadow);">
        <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 8px;">Total Balance</p>
        <h3 style="font-size: 18px; color: var(--text);">$12,450.00</h3>
      </div>
      <div style="background: var(--surface); padding: 16px; border-radius: 16px; box-shadow: 0 2px 8px var(--shadow);">
        <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 8px;">Monthly Savings</p>
        <h3 style="font-size: 18px; color: var(--text);">+$1,200.00</h3>
      </div>
    </div>

    <!-- Activity List -->
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h4 style="font-size: 16px; color: var(--text);">Recent Activity</h4>
        <button onclick="navigateTo('activity-log')" style="background: none; border: none; color: var(--primary); font-size: 14px;">View All</button>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <!-- inject: loop(recent_activities) -->
        <div onclick="navigateTo('detail', {id: 'act1'})" style="background: var(--surface); padding: 12px; border-radius: 12px; display: flex; align-items: center; gap: 12px;">
          <div style="width: 40px; height: 40px; border-radius: 8px; background: var(--surface-alt); display: flex; align-items: center; justify-content: center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20m10-10H2"/></svg>
          </div>
          <div style="flex: 1;">
            <p style="font-weight: 500; font-size: 14px; margin: 0;">Grocery Store</p>
            <p style="color: var(--text-muted); font-size: 12px; margin: 2px 0 0;">Today, 10:30 AM</p>
          </div>
          <p style="font-weight: 600; color: var(--error);">-$42.50</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## List Screen
Browseable collection of items with search and FAB.

```html
<section class="screen list-screen" style="background: var(--surface-alt); min-height: 100vh; padding-bottom: 80px;">
  <div style="position: sticky; top: 0; background: var(--surface); padding: 16px; border-bottom: 1px solid var(--border); z-index: 10;">
    <div style="position: relative;">
      <svg style="position: absolute; left: 12px; top: 12px; color: var(--text-muted);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" placeholder="Search items..." style="width: 100%; height: 44px; padding: 0 16px 0 44px; border-radius: 22px; border: 1px solid var(--border); background: var(--surface-alt); color: var(--text);">
    </div>
  </div>

  <div style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
    <!-- inject: loop(items) -->
    <div onclick="navigateTo('detail', {id: 'item1'})" style="background: var(--surface); border-radius: 16px; overflow: hidden; display: flex; box-shadow: 0 2px 8px var(--shadow);">
      <div style="width: 100px; background: #eee;">
        <!-- inject: item.thumbnail -->
        <div style="width:100%; height:100%; background: var(--primary-light);"></div>
      </div>
      <div style="flex: 1; padding: 16px;">
        <h3 style="font-size: 16px; margin: 0 0 4px; color: var(--text);">
          <!-- inject: item.title -->
          Modern Coffee Mug
        </h3>
        <p style="font-size: 14px; color: var(--text-muted); margin: 0 0 12px;">
          <!-- inject: item.subtitle -->
          Ceramic, 12oz matte finish
        </p>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: 600; color: var(--primary);">$24.00</span>
          <span style="font-size: 12px; background: var(--surface-alt); padding: 4px 8px; border-radius: 4px; color: var(--text-muted);">In Stock</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Floating Action Button -->
  <button onclick="navigateTo('add-new')" style="position: fixed; right: 24px; bottom: 100px; width: 56px; height: 56px; border-radius: 28px; background: var(--primary); color: white; border: none; box-shadow: 0 4px 12px var(--shadow-primary); display: flex; align-items: center; justify-content: center; z-index: 20;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M12 5v14M5 12h14"/></svg>
  </button>
</section>
```

---

## Detail Screen
Immersive view for a single entity with content sections and actions.

```html
<section class="screen detail-screen" style="background: var(--surface); min-height: 100vh; padding-bottom: 100px;">
  <div style="position: relative; height: 300px; background: #eee;">
    <!-- Hero Image -->
    <div style="width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0) 50%), var(--primary-light);"></div>
    
    <!-- Top Nav -->
    <div style="position: absolute; top: 0; left: 0; right: 0; padding: 16px; display: flex; justify-content: space-between;">
      <button onclick="navigateTo('back')" style="width: 40px; height: 40px; border-radius: 20px; background: rgba(255,255,255,0.8); border: none; display: flex; align-items: center; justify-content: center;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <button style="width: 40px; height: 40px; border-radius: 20px; background: rgba(255,255,255,0.8); border: none; display: flex; align-items: center; justify-content: center;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
      </button>
    </div>
  </div>

  <div style="padding: 24px; margin-top: -32px; background: var(--surface); border-radius: 32px 32px 0 0; position: relative;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
      <div>
        <h2 style="font-size: 24px; margin: 0 0 4px; color: var(--text);">
          <!-- inject: item.title -->
          Midnight Speaker
        </h2>
        <p style="color: var(--text-muted); font-size: 14px;">Premium Audio Experience</p>
      </div>
      <div style="font-size: 24px; font-weight: 700; color: var(--primary);">$199</div>
    </div>

    <div style="display: flex; gap: 12px; margin-bottom: 24px;">
      <div style="background: var(--surface-alt); padding: 8px 12px; border-radius: 8px; font-size: 13px; color: var(--text-muted);">Bluetooth 5.2</div>
      <div style="background: var(--surface-alt); padding: 8px 12px; border-radius: 8px; font-size: 13px; color: var(--text-muted);">24h Battery</div>
    </div>

    <h4 style="font-size: 16px; margin-bottom: 12px;">About</h4>
    <p style="color: var(--text-muted); line-height: 1.6; font-size: 15px; margin-bottom: 32px;">
      <!-- inject: item.description -->
      Engineered for deep bass and crystal clear highs, the Midnight Speaker brings concert-quality sound to any room in your home.
    </p>

    <!-- Bottom Actions -->
    <div style="position: fixed; bottom: 0; left: 0; right: 0; padding: 20px 24px; background: var(--surface); border-top: 1px solid var(--border); display: flex; gap: 16px; z-index: 30;">
      <button style="flex: 1; height: 56px; background: var(--primary); color: white; border: none; border-radius: 16px; font-weight: 600; font-size: 16px;">Add to Cart</button>
    </div>
  </div>
</section>
```

---

## Settings Screen
Grouped settings items with toggles and navigation.

```html
<section class="screen settings-screen" style="background: var(--surface-alt); min-height: 100vh;">
  <header style="padding: 48px 24px 24px; background: var(--surface);">
    <h1 style="font-size: 28px; margin: 0; color: var(--text);">Settings</h1>
  </header>

  <div style="padding: 24px 0;">
    <!-- Section -->
    <h3 style="padding: 0 24px; font-size: 13px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 8px;">Account</h3>
    <div style="background: var(--surface); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
      <div onclick="navigateTo('edit-profile')" style="padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border);">
        <span style="color: var(--text);">Edit Profile</span>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
      </div>
      <div style="padding: 16px 24px; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: var(--text);">Email Notifications</span>
        <!-- Toggle Switch -->
        <div style="width: 44px; height: 24px; background: var(--primary); border-radius: 12px; position: relative;">
          <div style="width: 20px; height: 20px; background: white; border-radius: 10px; position: absolute; right: 2px; top: 2px;"></div>
        </div>
      </div>
    </div>

    <!-- Section -->
    <h3 style="padding: 24px 24px 8px; font-size: 13px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em;">Preferences</h3>
    <div style="background: var(--surface); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
      <div style="padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border);">
        <span style="color: var(--text);">Dark Mode</span>
        <div style="width: 44px; height: 24px; background: var(--border); border-radius: 12px; position: relative;">
          <div style="width: 20px; height: 20px; background: white; border-radius: 10px; position: absolute; left: 2px; top: 2px;"></div>
        </div>
      </div>
    </div>

    <!-- Danger Zone -->
    <div style="margin-top: 48px; padding: 0 24px;">
      <button onclick="navigateTo('logout')" style="width: 100%; height: 52px; background: transparent; color: var(--error); border: 1px solid var(--error); border-radius: 12px; font-weight: 600;">Sign Out</button>
      <p style="text-align: center; font-size: 12px; color: var(--text-muted); margin-top: 16px;">App Version 1.2.0</p>
    </div>
  </div>
</section>
```

---

## Profile Screen
User overview with stats and content grid.

```html
<section class="screen profile-screen" style="background: var(--surface); min-height: 100vh;">
  <div style="padding: 40px 24px 24px; text-align: center;">
    <div style="width: 100px; height: 100px; border-radius: 50px; background: var(--primary-light); margin: 0 auto 16px; border: 4px solid var(--surface-alt); overflow: hidden;">
       <!-- inject: user.avatar -->
       <div style="width:100%; height:100%; background: var(--primary);"></div>
    </div>
    <h2 style="font-size: 22px; margin: 0; color: var(--text);">
      <!-- inject: user.name -->
      Sarah Jones
    </h2>
    <p style="color: var(--text-muted); font-size: 14px; margin: 4px 0 24px;">UI Designer & Traveler</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 24px;">
      <div>
        <div style="font-weight: 700; font-size: 18px;">128</div>
        <div style="font-size: 12px; color: var(--text-muted);">Posts</div>
      </div>
      <div>
        <div style="font-weight: 700; font-size: 18px;">2.4k</div>
        <div style="font-size: 12px; color: var(--text-muted);">Followers</div>
      </div>
      <div>
        <div style="font-weight: 700; font-size: 18px;">450</div>
        <div style="font-size: 12px; color: var(--text-muted);">Following</div>
      </div>
    </div>

    <button onclick="navigateTo('edit-profile')" style="width: 100%; height: 44px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface-alt); font-weight: 600; color: var(--text);">Edit Profile</button>
  </div>

  <!-- Content Grid -->
  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2px; background: var(--border);">
    <!-- inject: loop(posts) -->
    <div style="aspect-ratio: 1; background: var(--surface-alt); display: flex; align-items: center; justify-content: center;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
    </div>
    <div style="aspect-ratio: 1; background: var(--surface-alt);"></div>
    <div style="aspect-ratio: 1; background: var(--surface-alt);"></div>
    <div style="aspect-ratio: 1; background: var(--surface-alt);"></div>
    <div style="aspect-ratio: 1; background: var(--surface-alt);"></div>
    <div style="aspect-ratio: 1; background: var(--surface-alt);"></div>
  </div>
</section>
```

---

## Onboarding
Full-screen introductory pages with progress indicators.

```html
<section class="screen onboarding-screen" style="height: 100vh; display: flex; flex-direction: column; background: var(--surface);">
  <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px;">
    <div style="width: 280px; height: 280px; border-radius: 140px; background: var(--primary-light); margin-bottom: 48px; display: flex; align-items: center; justify-content: center;">
      <!-- Illustration Placeholder -->
      <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    </div>
    
    <h2 style="font-size: 26px; font-weight: 700; text-align: center; margin-bottom: 16px; color: var(--text);">Secure Your Assets</h2>
    <p style="text-align: center; color: var(--text-muted); line-height: 1.6; font-size: 16px;">Advanced encryption technology keeps your personal information safe and private at all times.</p>
  </div>

  <div style="padding: 40px; display: flex; flex-direction: column; align-items: center; gap: 32px;">
    <!-- Progress Dots -->
    <div style="display: flex; gap: 8px;">
      <div style="width: 24px; height: 8px; border-radius: 4px; background: var(--primary);"></div>
      <div style="width: 8px; height: 8px; border-radius: 4px; background: var(--border);"></div>
      <div style="width: 8px; height: 8px; border-radius: 4px; background: var(--border);"></div>
    </div>

    <div style="width: 100%; display: flex; justify-content: space-between; align-items: center;">
      <button onclick="navigateTo('login')" style="background: none; border: none; color: var(--text-muted); font-weight: 600; padding: 12px;">Skip</button>
      <button onclick="navigateTo('onboarding-2')" style="height: 52px; padding: 0 32px; border-radius: 12px; background: var(--primary); color: white; border: none; font-weight: 600;">Next</button>
    </div>
  </div>
</section>
```

---

## Modal/Bottom Sheet
Overlay panel for quick actions or additional context.

```html
<div class="overlay" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 100; display: flex; align-items: flex-end;">
  <section class="bottom-sheet" style="width: 100%; background: var(--surface); border-radius: 24px 24px 0 0; padding: 12px 24px 40px; animation: slideUp 0.3s ease-out;">
    <!-- Drag Handle -->
    <div style="width: 40px; height: 4px; background: var(--border); border-radius: 2px; margin: 0 auto 24px;"></div>
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h3 style="font-size: 20px; margin: 0; color: var(--text);">Share with friends</h3>
      <button onclick="closeModal()" style="width: 32px; height: 32px; border-radius: 16px; background: var(--surface-alt); border: none; display: flex; align-items: center; justify-content: center;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    </div>

    <div style="display: flex; flex-direction: column; gap: 8px;">
      <button style="height: 56px; width: 100%; padding: 0 16px; border-radius: 12px; background: var(--surface-alt); border: none; display: flex; align-items: center; gap: 12px; color: var(--text); font-weight: 500;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/></svg>
        Copy Link
      </button>
      <button style="height: 56px; width: 100%; padding: 0 16px; border-radius: 12px; background: var(--surface-alt); border: none; display: flex; align-items: center; gap: 12px; color: var(--text); font-weight: 500;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="m22 6-10 7L2 6"/></svg>
        Send via Email
      </button>
    </div>
  </section>
</div>
```

---

## Search Screen
Interactive search interface with recent history.

```html
<section class="screen search-screen" style="background: var(--surface); min-height: 100vh;">
  <div style="padding: 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border);">
    <button onclick="navigateTo('back')" style="background: none; border: none; color: var(--text);">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
    </button>
    <div style="flex: 1; position: relative;">
      <input type="text" autofocus placeholder="What are you looking for?" style="width: 100%; height: 44px; padding: 0 16px; border-radius: 12px; border: 1px solid var(--primary); background: var(--surface-alt); color: var(--text); font-size: 16px;">
    </div>
  </div>

  <div style="padding: 24px;">
    <h4 style="color: var(--text-muted); font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px;">Recent Searches</h4>
    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
      <!-- inject: loop(recent_searches) -->
      <div onclick="performSearch('Coffee')" style="padding: 8px 16px; background: var(--surface-alt); border-radius: 20px; font-size: 14px; color: var(--text); border: 1px solid var(--border);">Coffee</div>
      <div onclick="performSearch('Speakers')" style="padding: 8px 16px; background: var(--surface-alt); border-radius: 20px; font-size: 14px; color: var(--text); border: 1px solid var(--border);">Speakers</div>
      <div onclick="performSearch('Minimalist')" style="padding: 8px 16px; background: var(--surface-alt); border-radius: 20px; font-size: 14px; color: var(--text); border: 1px solid var(--border);">Minimalist</div>
    </div>
  </div>
</section>
```

---

## Empty State
User feedback when no data is available.

```html
<section class="screen empty-state" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; padding: 40px; text-align: center;">
  <div style="width: 160px; height: 160px; background: var(--surface-alt); border-radius: 80px; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
    <!-- Icon or Illustration -->
    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </div>
  
  <h2 style="font-size: 22px; margin-bottom: 8px; color: var(--text);">No messages yet</h2>
  <p style="color: var(--text-muted); line-height: 1.6; margin-bottom: 32px;">Start a conversation with your friends to see them appear here.</p>
  
  <button onclick="navigateTo('new-message')" style="height: 52px; padding: 0 32px; border-radius: 12px; background: var(--primary); color: white; border: none; font-weight: 600; font-size: 16px;">New Message</button>
</section>
```

---

## Tab Bar Layout
Persistent navigation at the bottom of the screen.

```html
<nav class="tab-bar" style="position: fixed; bottom: 0; left: 0; right: 0; height: 84px; background: var(--surface); border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; padding-bottom: 20px; z-index: 50;">
  <button onclick="navigateTo('home')" style="background: none; border: none; display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--primary);">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    <span style="font-size: 10px; font-weight: 600;">Home</span>
  </button>
  
  <button onclick="navigateTo('explore')" style="background: none; border: none; display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-muted);">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
    <span style="font-size: 10px;">Explore</span>
  </button>

  <button onclick="navigateTo('notifications')" style="background: none; border: none; display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-muted); position: relative;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
    <span style="font-size: 10px;">Alerts</span>
    <!-- Badge -->
    <div style="position: absolute; top: 0; right: 12px; width: 8px; height: 8px; border-radius: 4px; background: var(--error); border: 2px solid var(--surface);"></div>
  </button>

  <button onclick="navigateTo('settings')" style="background: none; border: none; display: flex; flex-direction: column; align-items: center; gap: 4px; color: var(--text-muted);">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/></svg>
    <span style="font-size: 10px;">Settings</span>
  </button>
</nav>
```
