Feature: Document themes
  As an author publishing Markus documents
  I want to apply themes such as hackerman, ristretto, gruvbox, lumon, tokyo-night, catppuccin-latte, flexoki-light, white, and osaka-jade
  So that documents render with cohesive palettes matching Antharchy / Omarchy

  Scenario: Front matter applies the hackerman theme to a full document
    Given the Markus source:
      """
      ---
      title: Cyberpunk Systems
      theme: hackerman
      ---

      # Terminal Access
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"
    And the HTML should contain "--markus-ink: #ddf7ff"
    And the HTML should contain "--markus-paper: #0B0C16"
    And the HTML should contain "--markus-accent: #82FB9C"

  Scenario: Front matter applies the hackerman theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Cyberpunk Systems
      theme: hackerman
      ---

      # Terminal Access
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"

  Scenario: Theme can be specified via conversion option
    Given the Markus source:
      """
      # Terminal Access
      """
    When I convert the source to an HTML fragment with theme "hackerman"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"

  Scenario: CLI convert with --theme applies hackerman theme
    Given a Markus file "hacker.md" with:
      """
      # Cyberdeck Initialized
      """
    When I run "markus convert hacker.md --theme hackerman"
    Then the command should succeed
    And stdout should contain "hackerman"
    And stdout should contain "--markus-ink: #ddf7ff"

  Scenario: Front matter applies the ristretto theme to a full document
    Given the Markus source:
      """
      ---
      title: Warm Coffee
      theme: ristretto
      ---

      # Espresso Notes
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ristretto"
    And the HTML should contain "--markus-ink: #e6d9db"
    And the HTML should contain "--markus-paper: #2c2525"
    And the HTML should contain "--markus-accent: #f38d70"

  Scenario: Front matter applies the ristretto theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Warm Coffee
      theme: ristretto
      ---

      # Espresso Notes
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ristretto"

  Scenario: Theme can be specified via conversion option for ristretto
    Given the Markus source:
      """
      # Espresso Notes
      """
    When I convert the source to an HTML fragment with theme "ristretto"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ristretto"

  Scenario: CLI convert with --theme applies ristretto theme
    Given a Markus file "coffee.md" with:
      """
      # Ristretto Shot
      """
    When I run "markus convert coffee.md --theme ristretto"
    Then the command should succeed
    And stdout should contain "ristretto"
    And stdout should contain "--markus-ink: #e6d9db"

  Scenario: Front matter applies the gruvbox theme to a full document
    Given the Markus source:
      """
      ---
      title: Forest Journal
      theme: gruvbox
      ---

      # Warm Earth
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "gruvbox"
    And the HTML should contain "--markus-ink: #d4be98"
    And the HTML should contain "--markus-paper: #282828"
    And the HTML should contain "--markus-accent: #7daea3"

  Scenario: Front matter applies the gruvbox theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Forest Journal
      theme: gruvbox
      ---

      # Warm Earth
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "gruvbox"

  Scenario: Theme can be specified via conversion option for gruvbox
    Given the Markus source:
      """
      # Warm Earth
      """
    When I convert the source to an HTML fragment with theme "gruvbox"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "gruvbox"

  Scenario: CLI convert with --theme applies gruvbox theme
    Given a Markus file "journal.md" with:
      """
      # Earthy Tones
      """
    When I run "markus convert journal.md --theme gruvbox"
    Then the command should succeed
    And stdout should contain "gruvbox"
    And stdout should contain "--markus-ink: #d4be98"

  Scenario: Front matter applies the lumon theme to a full document
    Given the Markus source:
      """
      ---
      title: Macrodata Refinement
      theme: lumon
      ---

      # Severed Floor
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lumon"
    And the HTML should contain "--markus-ink: #d6e2ee"
    And the HTML should contain "--markus-paper: #16242d"
    And the HTML should contain "--markus-accent: #8bc9eb"

  Scenario: Front matter applies the lumon theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Macrodata Refinement
      theme: lumon
      ---

      # Severed Floor
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lumon"

  Scenario: Theme can be specified via conversion option for lumon
    Given the Markus source:
      """
      # Severed Floor
      """
    When I convert the source to an HTML fragment with theme "lumon"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lumon"

  Scenario: CLI convert with --theme applies lumon theme
    Given a Markus file "macrodata.md" with:
      """
      # Cold Harbor
      """
    When I run "markus convert macrodata.md --theme lumon"
    Then the command should succeed
    And stdout should contain "lumon"
    And stdout should contain "--markus-ink: #d6e2ee"

  Scenario: Front matter applies the tokyo-night theme to a full document
    Given the Markus source:
      """
      ---
      title: Neon City
      theme: tokyo-night
      ---

      # Shinjuku Alley
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "tokyo-night"
    And the HTML should contain "--markus-ink: #a9b1d6"
    And the HTML should contain "--markus-paper: #1a1b26"
    And the HTML should contain "--markus-accent: #7aa2f7"

  Scenario: Front matter applies the tokyo-night theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Neon City
      theme: tokyo-night
      ---

      # Shinjuku Alley
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "tokyo-night"

  Scenario: Theme can be specified via conversion option for tokyo-night
    Given the Markus source:
      """
      # Shinjuku Alley
      """
    When I convert the source to an HTML fragment with theme "tokyo-night"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "tokyo-night"

  Scenario: CLI convert with --theme applies tokyo-night theme
    Given a Markus file "neon.md" with:
      """
      # Akihabara Lights
      """
    When I run "markus convert neon.md --theme tokyo-night"
    Then the command should succeed
    And stdout should contain "tokyo-night"
    And stdout should contain "--markus-ink: #a9b1d6"

  Scenario: Front matter applies the catppuccin-latte theme to a full document
    Given the Markus source:
      """
      ---
      title: Warm Coffee
      theme: catppuccin-latte
      ---

      # Latte Art
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin-latte"
    And the HTML should contain "--markus-ink: #4c4f69"
    And the HTML should contain "--markus-paper: #eff1f5"
    And the HTML should contain "--markus-accent: #1e66f5"

  Scenario: Front matter applies the catppuccin-latte theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Warm Coffee
      theme: catppuccin-latte
      ---

      # Latte Art
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin-latte"

  Scenario: Theme can be specified via conversion option for catppuccin-latte
    Given the Markus source:
      """
      # Latte Art
      """
    When I convert the source to an HTML fragment with theme "catppuccin-latte"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin-latte"

  Scenario: CLI convert with --theme applies catppuccin-latte theme
    Given a Markus file "latte.md" with:
      """
      # Sweet Milk
      """
    When I run "markus convert latte.md --theme catppuccin-latte"
    Then the command should succeed
    And stdout should contain "catppuccin-latte"
    And stdout should contain "--markus-ink: #4c4f69"

  Scenario: Front matter applies the flexoki-light theme to a full document
    Given the Markus source:
      """
      ---
      title: Warm Paper
      theme: flexoki-light
      ---

      # Botanical Notes
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "flexoki-light"
    And the HTML should contain "--markus-ink: #100F0F"
    And the HTML should contain "--markus-paper: #FFFCF0"
    And the HTML should contain "--markus-accent: #205EA6"

  Scenario: Front matter applies the flexoki-light theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Warm Paper
      theme: flexoki-light
      ---

      # Botanical Notes
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "flexoki-light"

  Scenario: Theme can be specified via conversion option for flexoki-light
    Given the Markus source:
      """
      # Botanical Notes
      """
    When I convert the source to an HTML fragment with theme "flexoki-light"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "flexoki-light"

  Scenario: CLI convert with --theme applies flexoki-light theme
    Given a Markus file "paper.md" with:
      """
      # Garden Sketches
      """
    When I run "markus convert paper.md --theme flexoki-light"
    Then the command should succeed
    And stdout should contain "flexoki-light"
    And stdout should contain "--markus-ink: #100F0F"

  Scenario: Front matter applies the white theme to a full document
    Given the Markus source:
      """
      ---
      title: Minimalist White
      theme: white
      ---

      # Clean Slate
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "white"
    And the HTML should contain "--markus-ink: #000000"
    And the HTML should contain "--markus-paper: #ffffff"
    And the HTML should contain "--markus-accent: #6e6e6e"

  Scenario: Front matter applies the white theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Minimalist White
      theme: white
      ---

      # Clean Slate
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "white"

  Scenario: Theme can be specified via conversion option for white
    Given the Markus source:
      """
      # Clean Slate
      """
    When I convert the source to an HTML fragment with theme "white"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "white"

  Scenario: CLI convert with --theme applies white theme
    Given a Markus file "white.md" with:
      """
      # Stark Paper
      """
    When I run "markus convert white.md --theme white"
    Then the command should succeed
    And stdout should contain "white"
    And stdout should contain "--markus-ink: #000000"

  Scenario: Front matter applies the osaka-jade theme to a full document
    Given the Markus source:
      """
      ---
      title: Bamboo Forest
      theme: osaka-jade
      ---

      # Temple Gardens
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "osaka-jade"
    And the HTML should contain "--markus-ink: #c1c497"
    And the HTML should contain "--markus-paper: #111c18"
    And the HTML should contain "--markus-accent: #509475"

  Scenario: Front matter applies the osaka-jade theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Bamboo Forest
      theme: osaka-jade
      ---

      # Temple Gardens
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "osaka-jade"

  Scenario: Theme can be specified via conversion option for osaka-jade
    Given the Markus source:
      """
      # Temple Gardens
      """
    When I convert the source to an HTML fragment with theme "osaka-jade"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "osaka-jade"

  Scenario: CLI convert with --theme applies osaka-jade theme
    Given a Markus file "bamboo.md" with:
      """
      # Emerald Pavilion
      """
    When I run "markus convert bamboo.md --theme osaka-jade"
    Then the command should succeed
    And stdout should contain "osaka-jade"
    And stdout should contain "--markus-ink: #c1c497"

  Scenario: Front matter applies the catppuccin theme to a full document
    Given the Markus source:
      """
      ---
      title: Catppuccin Mocha
      theme: catppuccin
      ---

      # Cozy Space
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin"
    And the HTML should contain "--markus-ink: #cdd6f4"
    And the HTML should contain "--markus-paper: #1e1e2e"
    And the HTML should contain "--markus-accent: #89b4fa"

  Scenario: Front matter applies the catppuccin theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Catppuccin Mocha
      theme: catppuccin
      ---

      # Cozy Space
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin"

  Scenario: Theme can be specified via conversion option for catppuccin
    Given the Markus source:
      """
      # Cozy Space
      """
    When I convert the source to an HTML fragment with theme "catppuccin"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "catppuccin"

  Scenario: CLI convert with --theme applies catppuccin theme
    Given a Markus file "mocha.md" with:
      """
      # Warm Catppuccin
      """
    When I run "markus convert mocha.md --theme catppuccin"
    Then the command should succeed
    And stdout should contain "catppuccin"
    And stdout should contain "--markus-ink: #cdd6f4"

  Scenario: Front matter applies the ethereal theme to a full document
    Given the Markus source:
      """
      ---
      title: Ethereal Dream
      theme: ethereal
      ---

      # Astral Plane
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ethereal"
    And the HTML should contain "--markus-ink: #ffcead"
    And the HTML should contain "--markus-paper: #060b1e"
    And the HTML should contain "--markus-accent: #7d82d9"

  Scenario: Front matter applies the ethereal theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Ethereal Dream
      theme: ethereal
      ---

      # Astral Plane
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ethereal"

  Scenario: Theme can be specified via conversion option for ethereal
    Given the Markus source:
      """
      # Astral Plane
      """
    When I convert the source to an HTML fragment with theme "ethereal"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "ethereal"

  Scenario: CLI convert with --theme applies ethereal theme
    Given a Markus file "ethereal.md" with:
      """
      # Cosmic Realm
      """
    When I run "markus convert ethereal.md --theme ethereal"
    Then the command should succeed
    And stdout should contain "ethereal"
    And stdout should contain "--markus-ink: #ffcead"

  Scenario: Front matter applies the everforest theme to a full document
    Given the Markus source:
      """
      ---
      title: Everforest Green
      theme: everforest
      ---

      # Deep Woods
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "everforest"
    And the HTML should contain "--markus-ink: #d3c6aa"
    And the HTML should contain "--markus-paper: #2d353b"
    And the HTML should contain "--markus-accent: #7fbbb3"

  Scenario: Front matter applies the everforest theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Everforest Green
      theme: everforest
      ---

      # Deep Woods
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "everforest"

  Scenario: Theme can be specified via conversion option for everforest
    Given the Markus source:
      """
      # Deep Woods
      """
    When I convert the source to an HTML fragment with theme "everforest"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "everforest"

  Scenario: CLI convert with --theme applies everforest theme
    Given a Markus file "forest.md" with:
      """
      # Pine Canopy
      """
    When I run "markus convert forest.md --theme everforest"
    Then the command should succeed
    And stdout should contain "everforest"
    And stdout should contain "--markus-ink: #d3c6aa"

  Scenario: Front matter applies the kanagawa theme to a full document
    Given the Markus source:
      """
      ---
      title: Kanagawa Wave
      theme: kanagawa
      ---

      # Great Wave
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "kanagawa"
    And the HTML should contain "--markus-ink: #dcd7ba"
    And the HTML should contain "--markus-paper: #1f1f28"
    And the HTML should contain "--markus-accent: #dcd7ba"

  Scenario: Front matter applies the kanagawa theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Kanagawa Wave
      theme: kanagawa
      ---

      # Great Wave
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "kanagawa"

  Scenario: Theme can be specified via conversion option for kanagawa
    Given the Markus source:
      """
      # Great Wave
      """
    When I convert the source to an HTML fragment with theme "kanagawa"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "kanagawa"

  Scenario: CLI convert with --theme applies kanagawa theme
    Given a Markus file "wave.md" with:
      """
      # Ocean Waves
      """
    When I run "markus convert wave.md --theme kanagawa"
    Then the command should succeed
    And stdout should contain "kanagawa"
    And stdout should contain "--markus-ink: #dcd7ba"

  Scenario: Front matter applies the last-horizon theme to a full document
    Given the Markus source:
      """
      ---
      title: Last Horizon
      theme: last-horizon
      ---

      # Distant Ridge
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "last-horizon"
    And the HTML should contain "--markus-ink: #fafcfb"
    And the HTML should contain "--markus-paper: #0c0b0c"
    And the HTML should contain "--markus-accent: #b59790"

  Scenario: Front matter applies the last-horizon theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Last Horizon
      theme: last-horizon
      ---

      # Distant Ridge
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "last-horizon"

  Scenario: Theme can be specified via conversion option for last-horizon
    Given the Markus source:
      """
      # Distant Ridge
      """
    When I convert the source to an HTML fragment with theme "last-horizon"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "last-horizon"

  Scenario: CLI convert with --theme applies last-horizon theme
    Given a Markus file "horizon.md" with:
      """
      # Twilight Edge
      """
    When I run "markus convert horizon.md --theme last-horizon"
    Then the command should succeed
    And stdout should contain "last-horizon"
    And stdout should contain "--markus-ink: #fafcfb"

  Scenario: Front matter applies the lupine theme to a full document
    Given the Markus source:
      """
      ---
      title: Lupine Bloom
      theme: lupine
      ---

      # Wildflower Meadow
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lupine"
    And the HTML should contain "--markus-ink: #212121"
    And the HTML should contain "--markus-paper: #fafafa"
    And the HTML should contain "--markus-accent: #3264eb"

  Scenario: Front matter applies the lupine theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Lupine Bloom
      theme: lupine
      ---

      # Wildflower Meadow
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lupine"

  Scenario: Theme can be specified via conversion option for lupine
    Given the Markus source:
      """
      # Wildflower Meadow
      """
    When I convert the source to an HTML fragment with theme "lupine"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "lupine"

  Scenario: CLI convert with --theme applies lupine theme
    Given a Markus file "lupine.md" with:
      """
      # Purple Petals
      """
    When I run "markus convert lupine.md --theme lupine"
    Then the command should succeed
    And stdout should contain "lupine"
    And stdout should contain "--markus-ink: #212121"

  Scenario: Front matter applies the matte-black theme to a full document
    Given the Markus source:
      """
      ---
      title: Matte Black Minimal
      theme: matte-black
      ---

      # Stealth Mode
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "matte-black"
    And the HTML should contain "--markus-ink: #bebebe"
    And the HTML should contain "--markus-paper: #121212"
    And the HTML should contain "--markus-accent: #e68e0d"

  Scenario: Front matter applies the matte-black theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Matte Black Minimal
      theme: matte-black
      ---

      # Stealth Mode
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "matte-black"

  Scenario: Theme can be specified via conversion option for matte-black
    Given the Markus source:
      """
      # Stealth Mode
      """
    When I convert the source to an HTML fragment with theme "matte-black"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "matte-black"

  Scenario: CLI convert with --theme applies matte-black theme
    Given a Markus file "stealth.md" with:
      """
      # Dark Carbon
      """
    When I run "markus convert stealth.md --theme matte-black"
    Then the command should succeed
    And stdout should contain "matte-black"
    And stdout should contain "--markus-ink: #bebebe"

  Scenario: Front matter applies the miasma theme to a full document
    Given the Markus source:
      """
      ---
      title: Miasma Fog
      theme: miasma
      ---

      # Swamp Mist
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "miasma"
    And the HTML should contain "--markus-ink: #c2c2b0"
    And the HTML should contain "--markus-paper: #222222"
    And the HTML should contain "--markus-accent: #78824b"

  Scenario: Front matter applies the miasma theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Miasma Fog
      theme: miasma
      ---

      # Swamp Mist
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "miasma"

  Scenario: Theme can be specified via conversion option for miasma
    Given the Markus source:
      """
      # Swamp Mist
      """
    When I convert the source to an HTML fragment with theme "miasma"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "miasma"

  Scenario: CLI convert with --theme applies miasma theme
    Given a Markus file "miasma.md" with:
      """
      # Murky Depths
      """
    When I run "markus convert miasma.md --theme miasma"
    Then the command should succeed
    And stdout should contain "miasma"
    And stdout should contain "--markus-ink: #c2c2b0"

  Scenario: Front matter applies the nord theme to a full document
    Given the Markus source:
      """
      ---
      title: Arctic Ice
      theme: nord
      ---

      # Polar Vista
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "nord"
    And the HTML should contain "--markus-ink: #d8dee9"
    And the HTML should contain "--markus-paper: #2e3440"
    And the HTML should contain "--markus-accent: #81a1c1"

  Scenario: Front matter applies the nord theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Arctic Ice
      theme: nord
      ---

      # Polar Vista
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "nord"

  Scenario: Theme can be specified via conversion option for nord
    Given the Markus source:
      """
      # Polar Vista
      """
    When I convert the source to an HTML fragment with theme "nord"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "nord"

  Scenario: CLI convert with --theme applies nord theme
    Given a Markus file "nord.md" with:
      """
      # Frozen Tundra
      """
    When I run "markus convert nord.md --theme nord"
    Then the command should succeed
    And stdout should contain "nord"
    And stdout should contain "--markus-ink: #d8dee9"

  Scenario: Front matter applies the retro-82 theme to a full document
    Given the Markus source:
      """
      ---
      title: Retro Eighty Two
      theme: retro-82
      ---

      # Vintage Neon
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "retro-82"
    And the HTML should contain "--markus-ink: #f6dcac"
    And the HTML should contain "--markus-paper: #05182e"
    And the HTML should contain "--markus-accent: #faa968"

  Scenario: Front matter applies the retro-82 theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Retro Eighty Two
      theme: retro-82
      ---

      # Vintage Neon
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "retro-82"

  Scenario: Theme can be specified via conversion option for retro-82
    Given the Markus source:
      """
      # Vintage Neon
      """
    When I convert the source to an HTML fragment with theme "retro-82"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "retro-82"

  Scenario: CLI convert with --theme applies retro-82 theme
    Given a Markus file "retro.md" with:
      """
      # Arcade Glow
      """
    When I run "markus convert retro.md --theme retro-82"
    Then the command should succeed
    And stdout should contain "retro-82"
    And stdout should contain "--markus-ink: #f6dcac"

  Scenario: Front matter applies the rose-pine theme to a full document
    Given the Markus source:
      """
      ---
      title: Rose Pine Dawn
      theme: rose-pine
      ---

      # Botanical Garden
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "rose-pine"
    And the HTML should contain "--markus-ink: #575279"
    And the HTML should contain "--markus-paper: #faf4ed"
    And the HTML should contain "--markus-accent: #56949f"

  Scenario: Front matter applies the rose-pine theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Rose Pine Dawn
      theme: rose-pine
      ---

      # Botanical Garden
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "rose-pine"

  Scenario: Theme can be specified via conversion option for rose-pine
    Given the Markus source:
      """
      # Botanical Garden
      """
    When I convert the source to an HTML fragment with theme "rose-pine"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "rose-pine"

  Scenario: CLI convert with --theme applies rose-pine theme
    Given a Markus file "rose.md" with:
      """
      # Petal Shadows
      """
    When I run "markus convert rose.md --theme rose-pine"
    Then the command should succeed
    And stdout should contain "rose-pine"
    And stdout should contain "--markus-ink: #575279"

  Scenario: Front matter applies the solitude theme to a full document
    Given the Markus source:
      """
      ---
      title: Quiet Solitude
      theme: solitude
      ---

      # Silent Chamber
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "solitude"
    And the HTML should contain "--markus-ink: #cacccc"
    And the HTML should contain "--markus-paper: #101315"
    And the HTML should contain "--markus-accent: #798186"

  Scenario: Front matter applies the solitude theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Quiet Solitude
      theme: solitude
      ---

      # Silent Chamber
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "solitude"

  Scenario: Theme can be specified via conversion option for solitude
    Given the Markus source:
      """
      # Silent Chamber
      """
    When I convert the source to an HTML fragment with theme "solitude"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "solitude"

  Scenario: CLI convert with --theme applies solitude theme
    Given a Markus file "solitude.md" with:
      """
      # Calm Serenity
      """
    When I run "markus convert solitude.md --theme solitude"
    Then the command should succeed
    And stdout should contain "solitude"
    And stdout should contain "--markus-ink: #cacccc"

  Scenario: Front matter applies the vantablack theme to a full document
    Given the Markus source:
      """
      ---
      title: Vantablack Void
      theme: vantablack
      ---

      # Pure Darkness
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "vantablack"
    And the HTML should contain "--markus-ink: #ffffff"
    And the HTML should contain "--markus-paper: #000000"
    And the HTML should contain "--markus-accent: #8d8d8d"

  Scenario: Front matter applies the vantablack theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Vantablack Void
      theme: vantablack
      ---

      # Pure Darkness
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "vantablack"

  Scenario: Theme can be specified via conversion option for vantablack
    Given the Markus source:
      """
      # Pure Darkness
      """
    When I convert the source to an HTML fragment with theme "vantablack"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "vantablack"

  Scenario: CLI convert with --theme applies vantablack theme
    Given a Markus file "vanta.md" with:
      """
      # Light Absorber
      """
    When I run "markus convert vanta.md --theme vantablack"
    Then the command should succeed
    And stdout should contain "vantablack"
    And stdout should contain "--markus-ink: #ffffff"

  Scenario: Unknown theme is rejected
    Given the Markus source:
      """
      ---
      title: Invalid Theme
      theme: non-existent-theme
      ---

      # Content
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown theme 'non-existent-theme'"

  Scenario: CLI rejects unknown theme
    Given a Markus file "test.md" with:
      """
      # Content
      """
    When I run "markus convert test.md --theme nonexistent"
    Then the command should fail
    And stderr should contain "Unknown theme 'nonexistent'"
