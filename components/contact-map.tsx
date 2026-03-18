export function ContactMap() {
  return (
    <section className="py-10">
      <div className="container px-4 md:px-6">
        <div className="w-full min-h-[400px] md:min-h-[600px] max-w-5xl mx-auto overflow-hidden rounded-lg shadow-lg">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2991.0!2d-74.4206521!3d41.4437301!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c33262597cb655%3A0x968db5356171d2eb!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1706810757943!5m2!1sen!2sus"
            width="100%"
            height="100%"
            style={{ border: 0 }}
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          ></iframe>
        </div>
      </div>
    </section>
  )
}

