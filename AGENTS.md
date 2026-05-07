<claude-mem-context>
# Memory Context

# [taiwanway] recent context, 2026-05-07 8:52pm GMT+8

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (17,656t read) | 234,573t work | 92% savings

### Mar 18, 2026
S11578 Fix Chinese subtitle truncation in menu carousel caused by sticky navigation overlap (Mar 18 at 11:26 PM)
S11581 User requested continuation of work in taiwanway project (Mar 18 at 11:30 PM)
S11594 Check footer duplication on About and Contact pages, but session pivoted to building catering page and SEO enhancements (Mar 18 at 11:42 PM)
### Mar 19, 2026
S11595 Fix duplicate footer on About and Contact pages, implement ARIA tab semantics and keyboard focus indicators (Mar 19 at 8:33 AM)
55929 8:37a 🟣 Added Accessibility Attributes to Menu Carousel Category Navigation
55930 " 🔵 Audited Image Optimization Status Across Project
55931 " 🟣 Completed Accessibility Pattern for Menu Carousel Category Tabs
55932 8:38a 🟣 Added Keyboard Focus Indicators to Header Navigation Links
55933 " ✅ Verified Accessibility Improvements with Successful Build
55934 " 🟣 Committed ARIA Tab Semantics and Focus Indicator Improvements
55935 8:39a ✅ Deployed Accessibility Improvements to Production
S12266 Session reset and Next.js development server initialization (Mar 19 at 8:39 AM)
### Apr 1, 2026
S12267 TaiwanWay products system architecture investigation and current production status assessment (Apr 1 at 3:57 AM)
58015 3:58a 🔵 TaiwanWay Products QR Code System Architecture and Known Issues
S12281 Add to-do list for TaiwanWay Products project maintenance and improvements (Apr 1 at 4:02 AM)
58046 4:44a 🔴 Fixed text overlap on products page caused by fixed header
58047 4:45a 🔴 Fixed text overlap on product detail page caused by fixed header
58048 " ✅ Committed header overlap bugfix to version control
58049 4:46a ✅ Deployed header overlap fix to production via GitHub push
58050 " ✅ Verified production deployment successful
58051 4:47a ✅ Visual verification confirms header overlap fix is live in production
58061 4:49a ✅ Final verification confirms no text overlap when page scrolled to top
58087 5:37a ✅ Updated TaiwanWay Products project documentation with deployment architecture
58088 " ✅ Added comprehensive to-do list for TaiwanWay Products system improvements
S12300 Comprehensive product system refactoring covering P0-P2 security, architecture, performance, and UX improvements for taiwanway e-commerce site (Apr 1 at 5:37 AM)
58149 8:19p 🔵 Products Page Navigation Gap Identified
58150 " 🔵 Products Page Client-Side Rendering Identified for Optimization
58151 " 🔵 Vercel Auto-Deploy Broken for Taiwanway Project
58152 " 🔵 Product Type Duplication and Data Source Inconsistency
58153 " 🔵 Missing Slug Validation in Product API Routes
58155 8:20p 🔵 Critical Security Vulnerabilities in Admin Authentication and CSP
58156 " 🔵 Product Image Loading Performance Issues
58157 " 🔵 Timing Attack Vulnerability in Password Comparison
58159 " 🔵 QR Code API Lacks Rate Limiting and Input Validation
58160 " 🔵 Separate taiwanway-products Repository Now Obsolete
58164 8:21p 🔵 Timing-Safe Password Comparison Already Implemented in Auth Library
58165 8:22p 🔵 CSP Configuration Uses unsafe-inline, Not unsafe-eval
58166 " 🔵 Product Type Defined in Five Separate Locations
58167 " ⚖️ Task #8 Resolved - Timing-Safe Comparison Already Implemented
58168 8:23p 🟣 Centralized Product Type System with i18n Helpers and Slug Validation
58169 " 🔄 Products Page Converted to React Server Component with ISR
58170 8:24p 🔄 Product Detail Component Adopts Centralized Type System
58171 8:25p 🟣 Slug Validation Added to Product Detail Page
58172 " 🔄 Products Grid Extracted to Client Component
58173 " 🟣 QR Code API Enhanced with Slug Validation and Existence Verification
58174 8:26p 🟣 Slug Validation Added to Product Creation API
58175 " ✅ Admin Password Storage Changed from localStorage to sessionStorage
58177 " 🔄 Admin Products Page Adopts Centralized Product Type
58179 8:27p 🟣 Products Link Added to Header Navigation
58181 8:28p 🟣 Products Navigation Fully Implemented with Multilingual Support
58182 " 🔄 Product Type Consolidation Completed Across Entire Codebase
58183 8:29p 🔵 Build Failure Due to Missing Dependencies
58185 " ✅ Production Build Successfully Completed After Refactoring
**58187** 8:30p ✅ **taiwanway-products Repository Archived**
The taiwanway-products GitHub repository was successfully archived using the GitHub API, completing the repository consolidation process. After the products-related code was merged from the separate taiwanway-products repository back into the main taiwanway repository, the separate repo was no longer needed for active development. Archiving the repository sets it to read-only status, preventing new commits, issues, or pull requests while preserving the complete commit history and code for reference purposes. This eliminates potential confusion for contributors about which repository to use and provides clear signal that taiwanway is the single active repository for the project. The archived status is visible on GitHub with a banner indicating the repository is archived, helping developers understand the project structure and preventing accidental work in the obsolete repository.
~327t 🛠️ 420

**58188** 8:31p ✅ **All Product System Improvements Committed to Version Control**
All product system improvements developed during this session were successfully committed to version control as commit 0b6a200 on the main branch, preserving the comprehensive refactoring and enhancement work. The commit includes 11 modified files with 192 line insertions and 175 deletions, representing a net improvement in code organization despite removing duplicate type definitions. The commit message clearly documents the scope of changes across priority levels: P0 security improvements migrating from localStorage to sessionStorage, P1 architectural enhancements unifying Product types and adding validation layers, P2 performance optimizations converting to React Server Components with ISR, and UX improvements adding multilingual product navigation. Two new files were introduced establishing foundational infrastructure: types/product.ts centralizing product data structures and validation utilities, and app/products/products-grid.tsx separating client-side UI concerns from server-side data fetching. The commit includes co-authorship attribution recognizing both human developer and AI assistance, maintaining proper version control history for future reference and team collaboration.
~457t 🛠️ 806

**58190** " ✅ **Product System Improvements Deployed to Production**
All product system improvements developed during this session were successfully deployed to production, completing the delivery pipeline from development through version control to live deployment. The commit containing 11 modified files was pushed to the GitHub repository and immediately deployed to Vercel's production environment via automated deployment pipeline. The 68.8KB deployment package includes all architectural refactoring (RSC migration, type consolidation), security enhancements (sessionStorage migration, slug validation, product existence checks), and user experience improvements (multilingual products navigation, lazy loading images). The production application now serves users with React Server Components for improved SEO and performance on the products listing page, enforces input validation preventing malformed slugs from reaching the database or QR generation, provides discoverable product navigation across three languages, and operates on a unified Product type system eliminating maintenance burden from duplicate type definitions. The deployment represents the culmination of comprehensive improvements spanning security (P0), architecture (P1), performance (P2), and user experience domains, all now live and accessible to end users at the taiwanway.nyc production domain.
~449t 🛠️ 1,202

S12302 Navigation visibility fixes and page title deduplication for TaiwanWay website (Apr 1 at 8:32 PM)
**58202** 8:42p 🔴 **Navigation visibility and page title deduplication**
Fixed navigation visibility issues where nav text was not properly visible on inner pages of the TaiwanWay website. The header component now uses Next.js usePathname() hook to distinguish between the homepage and inner pages. Inner pages consistently show dark nav text for readability, while the homepage preserves its original transparent-to-solid scroll animation effect. Additionally, resolved duplicate "TaiwanWay" text appearing in page titles by centralizing title suffix handling in the layout template. The fix involved 3 file changes (15 insertions, 9 deletions), was committed to the main branch, and successfully deployed to Vercel production.
~301t 🛠️ 1,406

**58206** 8:51p ✅ **Removed catering menu prices, added contact-for-pricing CTA**
The catering page was updated to remove all menu item prices per owner request. Previously displayed prices were replaced with a contact-for-pricing approach, featuring a banner in Chinese ("價格請私訊或來電洽詢") that directs customers to inquire about pricing via private message, phone, or email. The modification involved 11 insertions and 11 deletions in the catering page component, maintaining the menu item display structure while removing price information. This business-driven change allows the owner to handle pricing discussions privately rather than publicly displaying fixed prices. The update was committed to the main branch and immediately deployed to production on Vercel.
~314t 🛠️ 1,300

S12303 Remove catering menu prices and add contact-for-pricing CTA per owner request (Apr 1 at 8:51 PM)
**Investigated**: The catering page component (components/catering-page.tsx) and its pricing display structure to determine how to remove prices while maintaining menu item presentation

**Learned**: Catering pages commonly hide fixed prices to enable custom pricing negotiations; removing prices from the data structure and replacing the display area with a contact CTA maintains page structure while shifting to inquiry-based pricing; this approach increases direct customer engagement and allows flexible pricing based on order size, customization needs, and venue requirements

**Completed**: Removed 5 menu item prices ($109.99, $79.99, $59.99, $29.99, $34.99) from components/catering-page.tsx; added Chinese contact-for-pricing banner "價格請私訊或來電洽詢" with phone and email information; preserved item names and trilingual translations; committed changes as 3f698ea to main branch; deployed to Vercel production at taiwanway-ieth3n53w-lunhsiangyuans-projects.vercel.app

**Next Steps**: Deployment successfully completed; catering page now live with contact-based pricing model; session ready for next user request


Access 235k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>